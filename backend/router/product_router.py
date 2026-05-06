from fastapi import APIRouter, Body, Query
from schemas.base_response import Result
from schemas.product_schema import ProductSearchRequest, ProductListRead
from service.product_service.product_service import ProductService

router = APIRouter(prefix="/api/product", tags=["商品管理"])
product_service = ProductService()

@router.post("/list", response_model=Result[ProductListRead])
async def list_products(req: ProductSearchRequest):
    data = product_service.search_products(
        shop_ids=req.shop_ids,
        status=req.status,
        platform_item_id=req.platform_item_id, 
        page_no=req.page_no,
        page_size=req.page_size
    )
    return Result.success(data=data, msg="查询成功")

@router.get("/onsale-count", response_model=Result[int])
async def get_onsale_count(
    shop_id: str = Query(..., description="需要查询数量的店铺 ID")
):
    """
    获取指定店铺的在售商品总数
    """
    count = product_service.get_onsale_count(shop_id)
    return Result.success(data=count, msg="查询成功")