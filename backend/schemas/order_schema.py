from pydantic import BaseModel, Field
from typing import List, Optional, Dict

# --- 请求模型 ---
class OrderWarehouseCountRequest(BaseModel):
    shop_ids: Optional[List[str]] = Field(None, description="店铺 ID 列表", examples=[None])
    start_time: Optional[str] = Field(None, description="开始时间 YYYY-MM-DD HH:MM:SS", examples=[None])
    end_time: Optional[str] = Field(None, description="结束时间 YYYY-MM-DD HH:MM:SS", examples=[None])
    warehouse: Optional[str] = Field(None, description="仓库名称筛选", examples=[None])
    seller_sku: Optional[str] = Field(None, description="SKU 筛选", examples=[None])

# --- 🎯 响应模型：包含汇总统计 ---
class OrderWarehouseSummaryRead(BaseModel):
    stats: Dict[str, int] = Field(..., description="各仓库订单分布 (A-Z 排序)")
    total_orders: int = Field(..., description="符合筛选条件的订单总数")
    total_warehouses: int = Field(..., description="涉及的仓库总数")
    seller_skus: List[str] = Field(..., description="涉及的 Seller SKU 列表")