from fastapi import APIRouter
from typing import Dict
from schemas.base_response import Result
from schemas.order_schema import OrderWarehouseCountRequest, OrderWarehouseSummaryRead
from service.order_service.order_service import OrderService



router = APIRouter(prefix="/api/order", tags=["订单管理"])
order_service = OrderService()

@router.post("/warehouse-summary", response_model=Result[OrderWarehouseSummaryRead])
async def get_warehouse_summary(req: OrderWarehouseCountRequest):
    """
    按仓库获取订单数统计
    - 强制查询 waitShip (待发货) 状态
    - 返回包含汇总：总订单数、仓库总数及 A-Z 分布
    """
    summary_data = order_service.get_warehouse_order_counts(
        shop_ids=req.shop_ids,
        start_time=req.start_time,
        end_time=req.end_time,
        warehouse=req.warehouse,
        seller_sku=req.seller_sku
    )
    return Result.success(data=summary_data, msg="统计成功")