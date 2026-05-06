from fastapi import APIRouter, Query, HTTPException
from typing import List
from schemas.base_response import Result
from schemas.shop_schema import ShopRead
from service.shop_service import ShopService

# 初始化路由，设置前缀和标签
router = APIRouter(prefix="/api/shop", tags=["店铺管理"])

# 实例化业务层
shop_service = ShopService()

@router.get("/list", response_model=Result[List[ShopRead]])
async def list_shops():
    """
    获取当前账号绑定的所有店铺
    - 自动通过 @require_auth 获取 Cookie
    - 若未登录，底层 Service 或装饰器会触发相应的逻辑
    """
    shops = shop_service.get_all_shops()
    
    # 如果 shops 为 None 或由于认证问题无法获取，
    # 可以在这里根据业务需求返回 401，或者直接返回空列表
    if shops is None:
        return Result.fail(msg="获取店铺列表失败，请检查登录状态", code=401)
        
    return Result.success(data=shops, msg=f"成功获取 {len(shops)} 个店铺")


@router.get("/info", response_model=Result[ShopRead])
async def get_shop_detail(
    shop_id: str = Query(..., description="店铺唯一标识 ID")
):
    """
    获取单个店铺的详细信息 (带 Schema 校验)
    """
    info = shop_service.get_shop_info(shop_id)
    
    if info:
        return Result.success(data=info)
    
    # 若找不到该 ID 对应的店铺，返回 404 业务状态码
    return Result.fail(msg=f"未找到 ID 为 {shop_id} 的店铺信息", code=404)