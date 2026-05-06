from datetime import datetime
from .base_dao import BaseDao

class PriceDao(BaseDao):
    # =========================================================
    # 1. SKU 特价覆盖 (SKU Overrides)
    # =========================================================
    def get_sku_override(self, sku_id):
        """根据 SKU ID 获取特价"""
        with self._get_connection() as conn:
            res = conn.execute("SELECT special_price FROM sku_overrides WHERE sku_id = ?", (sku_id,)).fetchone()
            return res[0] if res else None

    def save_sku_override(self, sku_id, product_id, shop_id, special_price):
        """保存或更新 SKU 特价 (包含商品ID)"""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT INTO sku_overrides (sku_id, product_id, shop_id, special_price, update_time)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(sku_id) DO UPDATE SET 
                    product_id=excluded.product_id,
                    special_price=excluded.special_price,
                    update_time=excluded.update_time
            """, (sku_id, product_id, shop_id, special_price, now))

    def delete_sku_override(self, sku_id):
        """删除特价记录"""
        with self._get_connection() as conn:
            conn.execute("DELETE FROM sku_overrides WHERE sku_id = ?", (sku_id,))

    def get_all_overrides(self, shop_id):
        """获取全店特价列表 (给前端展示)"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT sku_id, product_id, special_price, update_time 
                FROM sku_overrides WHERE shop_id = ?
            """, (shop_id,))
            return [
                {"sku_id": r[0], "product_id": r[1], "special_price": r[2], "update_time": r[3]} 
                for r in cursor.fetchall()
            ]

    # =========================================================
    # 2. 价格策略与兜底 (Strategies & Bottom Limits)
    # =========================================================
    def get_active_strategies(self, shop_id):
        """获取计算类策略 (不含兜底价)，按优先级排序"""
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT id, keyword, rule_value, rule_type, priority FROM price_strategies 
                WHERE shop_id = ? AND rule_type NOT LIKE 'bottom_limit%' 
                ORDER BY priority DESC
            """, (shop_id,))
            
            strategies = []
            for row in cursor.fetchall():
                strategies.append({
                    "id": row[0],
                    "shop_id": shop_id,
                    "keyword": row[1],
                    "rule_value": row[2],
                    "rule_type": row[3],
                    "priority": row[4]
                })
            return strategies

    def get_shop_bottom_limit(self, shop_id):
        """
        获取兜底规则
        返回示例: {"value": 0.95, "type": "bottom_limit_ratio"}
        """
        with self._get_connection() as conn:
            res = conn.execute("""
                SELECT rule_value, rule_type FROM price_strategies 
                WHERE shop_id = ? AND rule_type IN ('bottom_limit_fixed', 'bottom_limit_ratio')
            """, (shop_id,)).fetchone()
            
            if res:
                return {"value": res[0], "type": res[1]}
            # 默认兜底：固定价 0.0 (即不限制)
            return {"value": 0.0, "type": "bottom_limit_fixed"}

    def get_shop_default_strategy(self, shop_id):
        """
        获取店铺的默认策略 (即 keyword 为空或 null 的记录)
        返回示例: {"value": 0.95, "type": "discount_rate"}
        """
        with self._get_connection() as conn:
            res = conn.execute("""
                SELECT rule_value, rule_type FROM price_strategies 
                WHERE shop_id = ? AND (keyword IS NULL OR keyword = '')
                AND rule_type NOT LIKE 'bottom_limit%'
                ORDER BY priority ASC LIMIT 1
            """, (shop_id,)).fetchone()
            
            if res:
                return {"value": res[0], "type": res[1]}
            
            return {"value": 0.95, "type": "discount_rate"}

    def save_strategy(self, strategy_data):
        """
        保存价格策略
        """
        strategy_id = strategy_data.get('id')
        
        with self._get_connection() as conn:
            if strategy_id:
                # 更新现有策略
                conn.execute("""
                    UPDATE price_strategies SET 
                        keyword = ?, 
                        rule_value = ?, 
                        rule_type = ?, 
                        priority = ?
                    WHERE id = ?
                """, (
                    strategy_data.get('keyword', ''),
                    strategy_data.get('rule_value', 0),
                    strategy_data.get('rule_type', 'discount_rate'),
                    strategy_data.get('priority', 0),
                    strategy_id
                ))
            else:
                # 插入新策略
                conn.execute("""
                    INSERT INTO price_strategies 
                    (shop_id, keyword, rule_value, rule_type, priority)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    strategy_data.get('shop_id'),
                    strategy_data.get('keyword', ''),
                    strategy_data.get('rule_value', 0),
                    strategy_data.get('rule_type', 'discount_rate'),
                    strategy_data.get('priority', 0)
                ))

    def delete_strategy(self, strategy_id):
        """
        删除价格策略
        """
        with self._get_connection() as conn:
            conn.execute("DELETE FROM price_strategies WHERE id = ?", (strategy_id,))
            conn.commit()