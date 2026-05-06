from typing import Dict, List, Optional
from dao.price_dao import PriceDao
from utils.logger_util import get_logger

logger = get_logger("PricePromotionService")

class PricePromotionService:
    def __init__(self):
        self.dao = PriceDao()

    def get_final_price(self, shop_id: str, sku_data: Dict) -> float: # 🎯 移除参数 default_rate
        """
        四级定价决策引擎：
        1. SKU 特价覆盖 (最高优先级)
        2. 关键词策略匹配 (AND/OR 逻辑)
        3. 店铺默认策略 (当无关键词匹配时，从数据库获取该店默认折扣)
        4. 兜底限价守门 (地板价校验，防止亏本)
        """
        original_price = float(sku_data.get("originalPrice", 0))
        sku_id = str(sku_data.get("platformSkuId"))
        sku_name = sku_data.get("skuSubName", "")
        
        # --- 1. SKU 特价覆盖 ---
        special = self.dao.get_sku_override(sku_id)
        if special: 
            return round(special, 2)

        # --- 2. 匹配关键词策略 ---
        final_price = self._match_strategies(shop_id, sku_name, original_price)
        
        # --- 3. 店铺默认策略 ---
        if final_price is None:
            default_info = self.dao.get_shop_default_strategy(shop_id) 
            val = default_info.get("value", 0.95)
            r_type = default_info.get("type", "discount_rate")
            final_price = self._calculate(original_price, val, r_type)

        # --- 4. 兜底限价守门 (地板价校验) ---
        limit_info = self.dao.get_shop_bottom_limit(shop_id)
        
        # 计算当前商品对应的“地板”是多少钱
        if limit_info["type"] == "bottom_limit_ratio":
            # 比例兜底：如 0.95，则地板价为原价的 95%
            floor_price = original_price * limit_info["value"]
        else:
            # 固定价兜底：如 5.5
            floor_price = limit_info["value"]

        # 触发兜底
        if final_price < floor_price:
            logger.info(f"触发兜底修正: SKU={sku_name}, 原价={original_price}, 计算价={final_price}, 地板价={floor_price}")
            final_price = floor_price

        # 确保不低于平台物理极限 $0.01
        return round(max(final_price, 0.01), 2)

    def _match_strategies(self, shop_id, sku_name, original_price) -> Optional[float]:
        """关键词匹配逻辑 (AND/OR)"""
        strategies = self.dao.get_active_strategies(shop_id)
        sku_name_lower = sku_name.lower()

        for strategy in strategies:
            kw_str = strategy.get('keyword', '')
            val = strategy.get('rule_value', 0)
            r_type = strategy.get('rule_type', 'discount_rate')
            
            if not kw_str:
                return self._calculate(original_price, val, r_type)

            # 且逻辑 (+)
            if "+" in kw_str:
                kws = [k.strip().lower() for k in kw_str.split("+") if k.strip()]
                is_match = all(k in sku_name_lower for k in kws)
            # 或逻辑 (,)
            else:
                kws = [k.strip().lower() for k in kw_str.split(",") if k.strip()]
                is_match = any(k in sku_name_lower for k in kws)
            
            if is_match:
                return self._calculate(original_price, val, r_type)
        return None

    def _calculate(self, original, value, r_type):
        """计算固定价或折扣"""
        return value if r_type == 'fixed_price' else (original * value)