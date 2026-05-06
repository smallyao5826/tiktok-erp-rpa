from typing import List, Dict, Optional
from client.order_client import OrderClient
from utils.logger_util import get_logger
from utils.decorators import require_auth

logger = get_logger("OrderService")

class OrderService:
    def __init__(self):
        self.client = OrderClient()

    @require_auth
    def get_warehouse_order_counts(
        self,
        shop_ids: Optional[List[str]] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        warehouse: Optional[str] = None,
        seller_sku: Optional[str] = None,
        cookie_str: str = None
    ) -> Dict:
        # --- 1. 数据防空清洗 (保持不变) ---
        shop_ids = None if not shop_ids or "string" in shop_ids else shop_ids
        start_time = None if start_time == "string" or not start_time else start_time
        end_time = None if end_time == "string" or not end_time else end_time
        warehouse = None if warehouse == "string" or not warehouse else warehouse
        seller_sku = None if seller_sku == "string" or not seller_sku else seller_sku
        
        # 转换日期格式：YYYY-MM-DD -> YYYY-MM-DD HH:MM:SS
        if start_time and len(start_time) == 10:
            start_time = f"{start_time} 00:00:00"
        if end_time and len(end_time) == 10:
            end_time = f"{end_time} 23:59:59"

        warehouse_stats = {}
        seller_skus = set()
        page_no = 1
        page_size = 100 
        TARGET_TAB = "waitShip"

        try:
            while True:
                res = self.client.search_order_package_list(
                    shop_ids=shop_ids,
                    page_no=page_no,
                    page_size=page_size,
                    start_time=start_time,
                    end_time=end_time,
                    tab=TARGET_TAB,
                    cookie_str=cookie_str
                )
                
                if res.get("result") != "success":
                    logger.error(f"查询订单包失败: {res.get('reason')}")
                    break
                
                packages = res.get("packageList", [])
                if not packages:
                    break
                
                for pkg in packages:
                    # 二次筛选逻辑 (保持不变)
                    agent_info = pkg.get("logisticsAgentProductInfo") or {}
                    warehouse_name = agent_info.get("warehouseName") or "未知仓库"
                    
                    if warehouse and warehouse != warehouse_name:
                        continue

                    items_map = pkg.get("items", {})
                    if seller_sku:
                        has_target_sku = any(
                            str(item.get("platformOuterSkuId")) == str(seller_sku) 
                            for item in items_map.values()
                        )
                        if not has_target_sku:
                            continue
                    
                    # 收集seller SKU
                    for item in items_map.values():
                        sku = item.get("platformOuterSkuId")
                        if sku:
                            seller_skus.add(str(sku))
                    
                    # 统计
                    warehouse_stats[warehouse_name] = warehouse_stats.get(warehouse_name, 0) + 1
                
                # 分页控制
                total = int(res.get("total", 0))
                if page_no * page_size >= total:
                    break
                page_no += 1
                
            # --- 2. 🎯 计算汇总数据与排序 ---
            sorted_stats = dict(sorted(warehouse_stats.items(), key=lambda x: x[0]))
            
            # 计算总和
            total_orders_count = sum(warehouse_stats.values())
            total_warehouses_count = len(warehouse_stats)
            sorted_seller_skus = sorted(list(seller_skus))

            return {
                "stats": sorted_stats,
                "total_orders": total_orders_count,
                "total_warehouses": total_warehouses_count,
                "seller_skus": sorted_seller_skus
            }

        except Exception as e:
            logger.exception(f"统计仓库订单数异常: {str(e)}")
            return {"stats": {}, "total_orders": 0, "total_warehouses": 0, "seller_skus": []}