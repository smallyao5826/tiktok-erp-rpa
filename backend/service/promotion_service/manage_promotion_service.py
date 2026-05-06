from typing import List, Dict, Optional
from .base_promotion_service import BasePromotionService
from utils.decorators import require_auth
from utils.logger_util import get_logger

logger = get_logger("ManagePromotionService")

class ManagePromotionService(BasePromotionService):
    def __init__(self):
        super().__init__()

    # =========================================================
    # 1. 批量更新活动价格 (策略重校准)
    # =========================================================
    @require_auth
    def batch_update_promotion_prices(
        self,
        shop_id: str,
        platform_promotion_ids: List[str],
        product_list: List[Dict],
        cookie_str: str = ""
    ) -> Dict:
        """
        批量为多个活动重新应用价格策略。
        适用于：当你修改了数据库里的关键词定价或兜底价，想一次性同步到多个活动时。
        """
        logger.info(f"[*] 开始批量更新价格策略：涉及活动数={len(platform_promotion_ids)}")
        
        optimized_payload = self._build_optimized_payload(
            shop_id=shop_id, 
            items=product_list, 
        )

        results = {"success": [], "fail": []}

        for p_id in platform_promotion_ids:
            try:
                # 调用基类的安全分批提交
                self._submit_products_in_batches(
                    shop_id=shop_id, 
                    promo_id=p_id, 
                    full_payload=optimized_payload, 
                    cookie=cookie_str
                )
                results["success"].append(p_id)
                logger.info(f"[√] 活动 {p_id} 价格更新成功")
            except Exception as e:
                results["fail"].append({"id": p_id, "reason": str(e)})
                logger.error(f"[x] 活动 {p_id} 价格更新失败: {str(e)}")

        return {
            "result": "success" if not results["fail"] else "partial_success",
            "report": results
        }

    # =========================================================
    # 2. 批量停用/下架活动
    # =========================================================
    @require_auth
    def batch_deactivate_promotions(
        self,
        shop_id: str,
        platform_promotion_ids: List[str],
        cookie_str: str = ""
    ) -> Dict:
        """
        批量停止多个活动。
        适用于：紧急下架、活动计划调整。
        """
        logger.warning(f"[!] 开始批量停用活动：涉及活动数={len(platform_promotion_ids)}")
        
        results = {"success": [], "fail": []}

        for p_id in platform_promotion_ids:
            res = self.promotion_client.deactivate_promotion(
                shop_id=shop_id,
                platform_promotion_id=p_id,
                cookie_str=cookie_str
            )
            
            if res.get("result") == "success":
                results["success"].append(p_id)
                logger.info(f"[√] 活动 {p_id} 已成功停用")
            else:
                results["fail"].append({"id": p_id, "reason": res.get("reason")})
                logger.error(f"[x] 活动 {p_id} 停用失败: {res.get('reason')}")
        
        return {
            "result": "success" if not results["fail"] else "partial_success",
            "report": results
        }

    # =========================================================
    # 3. 基础管理功能 (单体接口，供批量接口或直接调用)
    # =========================================================
    @require_auth
    def search_promotions(self, shop_ids=None, status="", title="", page_no=1, page_size=20, cookie_str="") -> Dict:
        """
        查询促销活动列表（支持标题搜索与数据清洗）
        """
        # 1. 调用 Client，增加 title 参数
        res = self.promotion_client.search_promotion_list(
            shop_ids=shop_ids, 
            status=status, 
            title=title, 
            page_no=page_no, 
            page_size=page_size, 
            cookie_str=cookie_str
        )
        
        if res.get("result") != "success":
            return {"list": [], "total": 0, "page": page_no, "page_size": page_size}

        # 2. 数据清洗逻辑（保持不变，确保返回给前端的字段精简）
        raw_list = res.get("promotionList", [])
        cleaned_list = []
        
        for p in raw_list:
            cleaned_list.append({
                "platform_promotion_id": p.get("platformPromotionId"),
                "title": p.get("title"),
                "status": p.get("status"),
                "gmt_local_begin": p.get("gmtLocalBegin"),
                "gmt_local_end": p.get("gmtLocalEnd"),
                "effective_item_count": int(p.get("effectiveItemCount", 0)),
                "effective_sku_count": int(p.get("effectiveSkuCount", 0)),
                "add_fail_item_count": int(p.get("addFailItemCount", 0))
            })
            
        return {
            "list": cleaned_list,
            "total": res.get("total", 0),
            "page": int(res.get("page", 1)),
            "page_size": int(res.get("pageSize", 20))
        }

    @require_auth
    def copy_existing_promotion(self, shop_id, platform_promotion_id, new_title, new_start, new_end, cookie_str="") -> Dict:
        copy_data = {
            "shopId": str(shop_id),
            "platformPromotionId": str(platform_promotion_id),
            "title": new_title,
            "gmtLocalBegin": new_start,
            "gmtLocalEnd": new_end
        }
        return self.promotion_client.copy_promotion(copy_data, cookie_str=cookie_str)

    # =========================================================
    # 4. 批量追加商品到活动
    # =========================================================
    @require_auth
    def batch_append_products_to_promotions(
        self,
        shop_id: str,
        platform_promotion_ids: List[str],
        platform_item_ids: List[str],
        cookie_str: str = ""
    ) -> Dict:
        """
        批量为多个活动追加商品。
        适用于：向现有活动添加新的商品。
        """
        logger.info(f"[*] 开始批量追加商品：涉及活动数={len(platform_promotion_ids)}, 商品数={len(platform_item_ids)}")
        
        # 1. 抓取指定的商品
        items = self._fetch_all_shop_items(
            shop_id=shop_id, 
            platform_item_ids=platform_item_ids, 
            cookie=cookie_str
        )
        
        if not items:
            logger.warning("[!] 未找到指定的商品")
            return {
                "result": "fail",
                "report": {"success": [], "fail": [{"id": "all", "reason": "未找到指定的商品"}]}
            }
        
        # 2. 构建优化后的 payload
        optimized_payload = self._build_optimized_payload(
            shop_id=shop_id, 
            items=items
        )

        # 3. 为每个活动追加商品
        results = {"success": [], "fail": []}

        for p_id in platform_promotion_ids:
            try:
                # 调用基类的安全分批提交
                errors = self._submit_products_in_batches(
                    shop_id=shop_id, 
                    promo_id=p_id, 
                    full_payload=optimized_payload, 
                    cookie=cookie_str
                )
                
                if not errors:
                    results["success"].append(p_id)
                    logger.info(f"[√] 活动 {p_id} 商品追加成功")
                else:
                    results["fail"].append({"id": p_id, "reason": f"部分商品添加失败: {len(errors)} 个"})
                    logger.error(f"[x] 活动 {p_id} 部分商品添加失败: {len(errors)} 个")
            except Exception as e:
                results["fail"].append({"id": p_id, "reason": str(e)})
                logger.error(f"[x] 活动 {p_id} 商品追加失败: {str(e)}")

        return {
            "result": "success" if not results["fail"] else "partial_success",
            "report": results
        }