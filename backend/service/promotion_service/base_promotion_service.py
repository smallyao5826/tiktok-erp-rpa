import re
import random
import string
import time
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import List, Dict, Optional

from client.promotion_client import PromotionClient
from service.promotion_service.price_promotion_service import PricePromotionService
from utils.logger_util import get_logger

class BasePromotionService:
    def __init__(self):
        # 初始化核心组件
        self.promotion_client = PromotionClient()
        self.price_service = PricePromotionService()
        self.logger = get_logger(self.__class__.__name__)
        
        # 平台硬性限制常量 (TikTok/妙手 API 规范)
        self.MAX_SKUS_PER_PROMOTION = 3000  # 单个活动最大允许包含的 SKU 总数
        self.MAX_SKUS_PER_API_CALL = 300   # 单次 add_or_update 接口建议的最大 SKU 数
        self.RETRY_DELAY = 1.0             # 分批提交之间的间隔时间 (秒)

    # =========================================================
    # 抓取店铺商品
    # =========================================================
    def _fetch_all_shop_items(self, shop_id: str, platform_item_ids: Optional[List[str]], cookie: str) -> List[Dict]:
        """
        全自动分页抓取店铺内所有待促销商品。
        :param platform_item_ids: 如果传入，则只返回这些指定的商品
        """
        all_items = []
        page_no = 1
        page_size = 500 # 尽量单次多拿，减少请求次数
        
        while True:
            self.logger.info(f"[*] 正在抓取店铺 {shop_id} 的候选商品 | 第 {page_no} 页")
            res = self.promotion_client.search_wait_add_promotion_item_list(
                shop_id, page_no, page_size, cookie_str=cookie
            )
            
            items = res.get("itemList", [])
            total = res.get("total", 0)
            
            if not items:
                break
                
            all_items.extend(items)
            
            # 判断是否已经抓完
            if len(all_items) >= total:
                break
            
            page_no += 1
            time.sleep(0.2) # 微小延迟，保护 API

        # 逻辑：如果有指定 ID 列表，则进行交集过滤
        if platform_item_ids:
            # 转为 set 提高查找效率
            id_set = set(str(pid) for pid in platform_item_ids)
            filtered_items = [i for i in all_items if str(i['platformItemId']) in id_set]
            self.logger.info(f"[√] 抓取完成：总数 {len(all_items)}，过滤后目标数 {len(filtered_items)}")
            return filtered_items
            
        self.logger.info(f"[√] 抓取完成：全店共计 {len(all_items)} 个候选商品")
        return all_items

    # =========================================================
    # 核心定价逻辑：将原始商品数据转换为带策略价格的 Payload
    # =========================================================
    def _build_optimized_payload(self, shop_id: str, items: List[Dict]) -> List[Dict]: # 🎯 移除参数
        """
        核心方法：遍历商品，完全依赖 PricePromotionService 决策价格。
        """
        payload = []
        for item in items:
            item_id = item.get("platformItemId")
            formatted_skus = []
            source_skus = item.get("skus") or item.get("skuList") or []
            
            for s in source_skus:
                # 🎯 核心调用：不再传入外部折扣
                final_price = self.price_service.get_final_price(
                    shop_id=shop_id,
                    sku_data=s
                )
                
                formatted_skus.append({
                    "platformSkuId": s["platformSkuId"],
                    "promotionPrice": final_price,
                    "skuSubName": s.get("skuSubName", "")
                })
            
            payload.append({
                "shopId": shop_id,
                "platformItemId": item_id,
                "skuList": formatted_skus
            })
        return payload

    # =========================================================
    # 平台限制处理：分批提交商品
    # =========================================================
    def _submit_products_in_batches(self, shop_id: str, promo_id: str, full_payload: List[Dict], cookie: str) -> List[Dict]:
        """
        分批提交并捕获具体的错误原因
        返回: [{"id": "xxx", "reason": "限流"}, ...]
        """
        all_errors = []
        cur_batch, cur_cnt = [], 0
        
        for item in full_payload:
            s_cnt = len(item['skuList'])
            if cur_cnt + s_cnt > self.MAX_SKUS_PER_API_CALL and cur_batch:
                res = self.promotion_client.add_or_update_promotion_discount_products(shop_id, promo_id, cur_batch, cookie)
                
                # 🎯 记录每一个失败的商品及其原因
                if res.get("errorProductList"):
                    for err in res["errorProductList"]:
                        all_errors.append({
                            "id": err.get("platformItemId"),
                            "reason": str(err.get("errorMsg") or err.get("failReason") or "")
                        })
                
                cur_batch, cur_cnt = [], 0
                time.sleep(0.5)
            
            cur_batch.append(item)
            cur_cnt += s_cnt
            
        if cur_batch:
            res = self.promotion_client.add_or_update_promotion_discount_products(shop_id, promo_id, cur_batch, cookie)
            if res.get("errorProductList"):
                for err in res["errorProductList"]:
                    all_errors.append({
                        "id": err.get("platformItemId"),
                        "reason": str(err.get("errorMsg") or err.get("failReason") or "")
                    })
        
        return all_errors

    def _add_products_with_retry(self, shop_id: str, promo_id: str, full_payload: List[Dict], cookie: str, max_retries: int = 3) -> bool:
        """
        根据错误原因决定是否重试：包含限流、超时、服务忙等暂时性错误
        """
        # 1. 第一轮常规提交
        errors = self._submit_products_in_batches(shop_id, promo_id, full_payload, cookie)
        if not errors:
            return True # 全部成功

        # 2. 定义可重试的关键字列表 (涵盖限流、超时、系统繁忙等)
        retryable_keywords = [
            "限流","系统错误", 
        ]
        
        # 筛选出属于暂时性故障、值得重试的商品 ID
        retry_ids = [
            e["id"] for e in errors 
            if any(k.lower() in e["reason"].lower() for k in retryable_keywords)
        ]
        
        # 记录那些“致命”错误 (如：活动冲突、价格违规、参数错误)，这些重试也没用
        fatal_errors = [e for e in errors if e["id"] not in retry_ids]
        if fatal_errors:
            for fe in fatal_errors:
                self.logger.error(f"[x] 致命错误(停止重试) | 商品: {fe['id']} | 原因: {fe['reason']}")
            # 如果存在哪怕一个致命错误，为了保证逻辑严谨，通常建议直接返回失败
            return False

        # 3. 进入重试循环
        retry_idx = 0
        while retry_ids and retry_idx < max_retries:
            retry_idx += 1
            # 采用指数退避策略：重试间隔随次数增加
            wait_time = 5 * retry_idx 
            self.logger.warning(f"[!] 触发暂时性错误重试 | 活动 {promo_id} | 第 {retry_idx} 次 | 等待 {wait_time}s")
            
            time.sleep(wait_time) 
            
            # 调用重试接口
            res = self.promotion_client.retry_add_promotion_items(shop_id, promo_id, retry_ids, cookie)
            
            # 更新需要继续重试的列表
            if res.get("result") == "fail" and "productIdAndFailRetMap" in res:
                # 重新判定失败原因，是否依然是可重试的
                new_retry_ids = []
                for pid, reason in res["productIdAndFailRetMap"].items():
                    if any(k.lower() in str(reason).lower() for k in retryable_keywords):
                        new_retry_ids.append(pid)
                    else:
                        self.logger.error(f"[x] 重试中发现致命错误 | 商品: {pid} | 原因: {reason}")
                retry_ids = new_retry_ids
            else:
                retry_ids = [] # 全部重试成功
        
        return len(retry_ids) == 0

    # =========================================================
    # 业务工具：SKU 分桶 (3000 SKU 限制)
    # =========================================================
    def _partition_items_by_sku_limit(self, items: List[Dict]) -> List[List[Dict]]:
        """
        如果一个店铺有上万个 SKU，TikTok 单个活动只能放 3000 个。
        该方法将商品列表切分为多个“活动桶”，确保同一个商品的 SKU 都放在同一个桶里。
        """
        buckets = []
        current_bucket = []
        current_sku_sum = 0
        
        for item in items:
            skus = item.get("skus") or item.get("skuList") or []
            s_count = len(skus)
            
            # 确保同一个商品的 SKU 都放在同一个桶里
            if current_sku_sum + s_count > self.MAX_SKUS_PER_PROMOTION:
                buckets.append(current_bucket)
                current_bucket = [item]
                current_sku_sum = s_count
            else:
                current_bucket.append(item)
                current_sku_sum += s_count
                
        if current_bucket:
            buckets.append(current_bucket)
        return buckets

    # =========================================================
    # 国际化工具：时区转换与标题生成
    # =========================================================
    def _convert_pst_to_ny(self, time_str: str) -> str:
        """PST (洛杉矶) 时间转 NY (纽约) 时间"""
        try:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            dt_pst = dt.replace(tzinfo=ZoneInfo("America/Los_Angeles"))
            dt_ny = dt_pst.astimezone(ZoneInfo("America/New_York"))
            return dt_ny.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            self.logger.error(f"时间转换失败: {str(e)}")
            return time_str

    def _generate_title(self, shop_nick: str, start_time: str, end_time: str, suffix: str = "") -> str:
        """
        生成符合运营核对习惯的标题。
        格式要求：
        1. 有店铺名：店铺简名-闪购-年.月.日-00:00-00:59-随机码
        2. 无店铺名：闪购-年.月.日-00:00-00:59-随机码
        """
        # 1. 解析时间
        dt_s = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        dt_e = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
        
        # 2. 构造日期和时间标签
        date_tag = f"{dt_s.year}.{dt_s.month}.{dt_s.day}"
        time_tag = f"{dt_s.strftime('%H:%M')}-{dt_e.strftime('%H:%M')}"
        
        # 3. 提取店铺简名并初始化组件列表
        components = []
        if shop_nick:
            # 按照空格、中划线、下划线、& 符号切分，取第一段作为简名
            short_name = re.split(r'[ \-_&]', shop_nick)[0]
            if short_name:
                components.append(short_name)
        
        # 无论有没有店铺名，都要加上“闪购”
        components.append("闪购")
        
        # 4. 加入日期和时间
        components.append(date_tag)
        components.append(time_tag)
        
        # 5. 如果有后缀则加入后缀
        if suffix:
            components.append(suffix)
        
        # 6. 生成 2 位随机码并加入
        rand = ''.join(random.choices(string.ascii_uppercase, k=2))
        components.append(rand)
        
        # 7. 最终拼接并限制 50 字符
        final_title = "-".join(components)
        return final_title[:50]