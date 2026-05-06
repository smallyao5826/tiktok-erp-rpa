from typing import List, Dict, Optional
import time
import asyncio
from .base_promotion_service import BasePromotionService
from service.shop_service import ShopService
from dao.webhook_dao import WebhookDao
from utils.webhook_util import WebhookUtil
from utils.decorators import require_auth
from utils.logger_util import get_logger

logger = get_logger("AddPromotionService")

class AddPromotionService(BasePromotionService):
    def __init__(self):
        # 1. 继承基类的 promotion_client, price_service 和通用的工具能力
        super().__init__()
        # 2. 注入店铺服务，用于溯源站点和昵称
        self.shop_service = ShopService()
        # 3. 任务队列，用于异步处理
        self.task_queue = []

    def _check_product_uniqueness(self, shop_id: str, items: List[Dict], cookie_str=None) -> Dict:
        """
        校验商品和SKU的唯一性，确保同一个商品不能同时参与多个活动
        """
        # 同步最新的促销状态
        self.promotion_client.rsync_full_shop_promotion([shop_id], cookie_str=cookie_str)
        
        # 获取店铺所有进行中和未开始的活动
        all_promotions = []
        page_no = 1
        page_size = 100
        
        while True:
            res = self.promotion_client.search_promotion_list(
                shop_ids=[shop_id],
                status="",  # 获取所有状态的活动
                page_no=page_no,
                page_size=page_size,
                cookie_str=cookie_str
            )
            
            if res.get("result") == "success":
                data = res.get("data", {})
                list_data = data.get("list", [])
                all_promotions.extend(list_data)
                
                # 检查是否还有更多数据
                total = data.get("total", 0)
                if len(all_promotions) >= total:
                    break
                page_no += 1
            else:
                break
        
        # 构建已参与活动的商品和SKU映射
        product_in_promotion = set()
        sku_in_promotion = set()
        
        for promotion in all_promotions:
            # 只检查进行中和未开始的活动
            promotion_status = promotion.get("status")
            if promotion_status in [1, 2]:  # 1: 未开始, 2: 进行中
                # 直接从活动数据中获取商品信息
                product_list = promotion.get("productList", [])
                for item in product_list:
                    product_id = item.get("platformItemId")
                    sku_id = item.get("platformSkuId")
                    if product_id:
                        product_in_promotion.add(product_id)
                    if sku_id:
                        sku_in_promotion.add(sku_id)
        
        # 检查当前要添加的商品是否已在其他活动中
        conflicting_products = []
        conflicting_skus = []
        
        for item in items:
            product_id = item.get("platformItemId")
            if product_id in product_in_promotion:
                conflicting_products.append(product_id)
            
            # 检查所有SKU
            for sku in item.get("skus", []):
                sku_id = sku.get("platformSkuId")
                if sku_id in sku_in_promotion:
                    conflicting_skus.append(sku_id)
        
        return {
            "has_conflict": len(conflicting_products) > 0 or len(conflicting_skus) > 0,
            "conflicting_products": conflicting_products,
            "conflicting_skus": conflicting_skus
        }

    async def _process_flash_sale_task(self, shop_id: str, time_slots: List[Dict[str, str]], platform_item_ids: Optional[List[str]], cookie_str=None):
        """
        异步处理闪购创建任务
        """
        start_time = time.time()
        webhook_dao = WebhookDao()
        
        try:
            # 发送开始 Webhook 通知
            webhooks = webhook_dao.get_enabled_webhooks()
            if webhooks:
                start_data = {
                    "event": "promotion_start",
                    "shop_id": shop_id,
                    "time_slots": time_slots,
                    "platform_item_ids": platform_item_ids,
                    "timestamp": time.time()
                }
                WebhookUtil.send_webhook_batch(webhooks, start_data)
            
            # --- 第一步：店铺溯源 ---
            # 获取站点信息 (用于判断是否执行 PST->NY 时间转换)
            shop_info = self.shop_service.get_shop_info(target_id=shop_id, cookie_str=cookie_str)
            if not shop_info:
                # 发送错误 Webhook 通知
                webhooks = webhook_dao.get_enabled_webhooks()
                if webhooks:
                    error_data = {
                        "event": "promotion_error",
                        "shop_id": shop_id,
                        "elapsed_time": time.time() - start_time,
                        "error": f"未能在账号下找到店铺 {shop_id}",
                        "timestamp": time.time()
                    }
                    WebhookUtil.send_webhook_batch(webhooks, error_data)
                return
            
            shop_nick = shop_info["shopNick"]
            is_us = (shop_info["site"] == "US")

            # --- 第二步：商品数据准备 ---
            logger.info(f"[*] 正在为店铺 {shop_nick} 准备促销数据包...")
            
            #  调用基类方法：全自动分页抓取并过滤目标商品
            raw_items = self._fetch_all_shop_items(shop_id, platform_item_ids, cookie=cookie_str)
            if not raw_items:
                # 发送错误 Webhook 通知
                webhooks = webhook_dao.get_enabled_webhooks()
                if webhooks:
                    error_data = {
                        "event": "promotion_error",
                        "shop_id": shop_id,
                        "elapsed_time": time.time() - start_time,
                        "error": "未找到符合条件的促销商品",
                        "timestamp": time.time()
                    }
                    WebhookUtil.send_webhook_batch(webhooks, error_data)
                return

            # --- 第三步：商品唯一性校验 ---
            uniqueness_check = self._check_product_uniqueness(shop_id, raw_items, cookie_str=cookie_str)
            if uniqueness_check["has_conflict"]:
                # 发送错误 Webhook 通知
                webhooks = webhook_dao.get_enabled_webhooks()
                if webhooks:
                    error_data = {
                        "event": "promotion_error",
                        "shop_id": shop_id,
                        "elapsed_time": time.time() - start_time,
                        "error": f"商品或SKU已参与其他活动，冲突商品: {uniqueness_check['conflicting_products']}, 冲突SKU: {uniqueness_check['conflicting_skus']}",
                        "timestamp": time.time()
                    }
                    WebhookUtil.send_webhook_batch(webhooks, error_data)
                return

            #  调用基类方法：根据 3000 SKU 限制将商品分桶 (Bucket)
            buckets = self._partition_items_by_sku_limit(raw_items)
            logger.info(f"[*] 分桶完成：共 {len(raw_items)} 个商品，拆分为 {len(buckets)} 个活动桶")

            # --- 第四步：创建首个时段 (Master 活动) ---
            first_raw_slot = time_slots[0]
            
            # 计算 API 提交时间 (美国站自动转纽约时间)
            api_slot = {
                "start": self._convert_pst_to_ny(first_raw_slot['start']) if is_us else first_raw_slot['start'],
                "end": self._convert_pst_to_ny(first_raw_slot['end']) if is_us else first_raw_slot['end']
            }

            master_promo_ids = []
            logger.info(f"[*] 正在创建主模板活动 | 基准时段: {first_raw_slot['start']}")

            for idx, bucket_items in enumerate(buckets):
                title = self._generate_title(shop_nick, first_raw_slot['start'], first_raw_slot['end'], f"S{idx+1}")
                
                # A. 创建活动空壳
                res = self.promotion_client.add_multi_shop_promotion(
                    [shop_id], title, api_slot['start'], api_slot['end'], cookie_str=cookie_str
                )
                promo_id = res.get("shopIdAndPlatformPromotionIdMap", {}).get(shop_id)
                
                if promo_id:
                    # B. 构建策略定价数据
                    payload = self._build_optimized_payload(shop_id, bucket_items)
                    
                    # C. 🎯 使用带重试机制的提交方法，并检查最终结果
                    success = self._add_products_with_retry(shop_id, promo_id, payload, cookie=cookie_str)
                    
                    if success:
                        master_promo_ids.append(promo_id)
                        logger.info(f"[√] Master 活动 {promo_id} 商品加载成功")
                    else:
                        # 如果商品死活加不进去，这个 Master 就不能作为 Copy 的模板
                        logger.error(f"[x] Master 活动 {promo_id} 商品加载失败，跳过此桶")
            
            if not master_promo_ids:
                # 发送错误 Webhook 通知
                webhooks = webhook_dao.get_enabled_webhooks()
                if webhooks:
                    error_data = {
                        "event": "promotion_error",
                        "shop_id": shop_id,
                        "elapsed_time": time.time() - start_time,
                        "error": "Master 活动创建失败，请检查妙手后台权限",
                        "timestamp": time.time()
                    }
                    WebhookUtil.send_webhook_batch(webhooks, error_data)
                return

            # 初始化报告数据
            report = {
                "success_slots": [{"slot": first_raw_slot['start'], "ids": master_promo_ids, "type": "master"}]
            }

            # --- 第五步：后续时段快速复制 ---
            if len(time_slots) > 1:
                for next_slot in time_slots[1:]:
                    # 计算下个时段的 API 提交时间
                    next_api_start = self._convert_pst_to_ny(next_slot['start']) if is_us else next_slot['start']
                    next_api_end = self._convert_pst_to_ny(next_slot['end']) if is_us else next_slot['end']
                    
                    copied_ids = []
                    # 遍历 Master IDs 进行组团复制
                    for idx, m_id in enumerate(master_promo_ids):
                        new_title = self._generate_title(shop_nick, next_slot['start'], next_slot['end'], f"S{idx+1}")
                        
                        copy_res = self.promotion_client.copy_promotion({
                            "shopId": shop_id,
                            "platformPromotionId": m_id,
                            "gmtLocalBegin": next_api_start,
                            "gmtLocalEnd": next_api_end,
                            "title": new_title
                        }, cookie_str=cookie_str)
                        
                        if copy_res.get("result") == "success":
                            new_pid = copy_res.get("shopIdAndPlatformPromotionIdMap", {}).get(shop_id)
                            copied_ids.append(new_pid or "COPIED")
                    
                    report["success_slots"].append({
                        "slot": next_slot['start'], "ids": copied_ids, "type": "copy"
                    })
                    logger.info(f"时段 {next_slot['start']} 复制成功")

            # 计算耗时
            elapsed_time = time.time() - start_time
            
            # 发送结束 Webhook 通知
            webhooks = webhook_dao.get_enabled_webhooks()
            if webhooks:
                end_data = {
                    "event": "promotion_end",
                    "shop_id": shop_id,
                    "shop_nick": shop_nick,
                    "elapsed_time": elapsed_time,
                    "report": report,
                    "status": "success",
                    "timestamp": time.time()
                }
                WebhookUtil.send_webhook_batch(webhooks, end_data)
            
            logger.info(f"[√] 闪购创建任务完成，耗时 {elapsed_time:.2f} 秒")

        except Exception as e:
            # 计算耗时
            elapsed_time = time.time() - start_time
            
            # 发送错误 Webhook 通知
            webhooks = webhook_dao.get_enabled_webhooks()
            if webhooks:
                error_data = {
                    "event": "promotion_error",
                    "shop_id": shop_id,
                    "elapsed_time": elapsed_time,
                    "error": str(e),
                    "timestamp": time.time()
                }
                WebhookUtil.send_webhook_batch(webhooks, error_data)
            
            logger.exception("AddPromotionService 流程发生严重异常")

    @require_auth
    def create_batch_flash_sales(
        self, 
        shop_id: str,
        time_slots: List[Dict[str, str]], 
        platform_item_ids: Optional[List[str]] = None,
        cookie_str=None
    ) -> Dict:
        """
        闪购创建指挥官：
        负责协调抓取、定价、创建模板活动以及跨时段批量复制。
        """
        # 立即返回任务已下发的响应
        logger.info(f"[*] 闪购任务已下发，开始异步处理 | 店铺: {shop_id}")
        
        # 异步执行闪购创建任务
        asyncio.create_task(self._process_flash_sale_task(shop_id, time_slots, platform_item_ids, cookie_str))
        
        # 立即返回成功响应，告知任务已下发
        return {"result": "success", "message": "任务已下发，请稍后关注TikTok后台或者妙手"}