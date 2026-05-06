from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Query, Body
from schemas.base_response import Result
from schemas.promotion_schema import (
    CreateFlashSaleRequest, AddUpdateProductRequest, PromotionCopyRequest,
    BatchDeactivateRequest, AppendProductsRequest, StrategySchema, SkuOverrideSchema, PromotionItemRead, PromotionListRead
)
from service.promotion_service.add_promotion_service import AddPromotionService
from service.promotion_service.manage_promotion_service import ManagePromotionService
from dao.price_dao import PriceDao

router = APIRouter(prefix="/api/promotion", tags=["促销与策略管理"])

add_service = AddPromotionService()
manage_service = ManagePromotionService()
price_dao = PriceDao()

# =========================================================
# 1. 促销活动核心操作 (创建、复制、更新商品、停用)
# =========================================================

@router.post("/flash-sale/create", response_model=Result[Dict])
async def create_flash_sales(req: CreateFlashSaleRequest):
    """
    一键分桶创建闪购任务
    - 折扣率将根据策略表自动计算 (特价 > 关键词策略 > 默认兜底)
    """
    slots = [slot.dict() for slot in req.time_slots]
    
    res = add_service.create_batch_flash_sales(
        shop_id=req.shop_id, 
        time_slots=slots,
        platform_item_ids=req.platform_item_ids,
    )
    
    if res.get("result") == "success":
        return Result.success(data=None, msg=res.get("message", "闪购创建任务已启动"))
    
    return Result.fail(msg=res.get("reason", "任务创建失败"))

@router.post("/product/add-update", response_model=Result[Dict])
async def add_update_products(req: AddUpdateProductRequest):
    """为特定活动添加/更新商品及策略定价"""
    res = manage_service.batch_update_promotion_prices(
        shop_id=req.shop_id,
        platform_promotion_ids=[req.platform_promotion_id],
        product_list=req.product_list,
        default_rate=req.default_rate
    )
    return Result.success(data=res.get("report"))

@router.post("/copy", response_model=Result[Dict])
async def copy_promotion(req: PromotionCopyRequest):
    """复制现有活动到新时段"""
    res = manage_service.copy_existing_promotion(
        shop_id=req.shop_id,
        platform_promotion_id=req.platform_promotion_id,
        new_title=req.new_title,
        new_start=req.new_start,
        new_end=req.new_end
    )
    return Result.success(data=res)

@router.post("/deactivate", response_model=Result[Dict])
async def deactivate_promotions(req: BatchDeactivateRequest):
    """批量下架/停止促销活动"""
    res = manage_service.batch_deactivate_promotions(
        shop_id=req.shop_id,
        platform_promotion_ids=req.platform_promotion_ids
    )
    return Result.success(data=res.get("report"))

@router.post("/append", response_model=Result[Dict])
async def append_products_to_promotions(req: AppendProductsRequest):
    """批量追加商品到活动"""
    res = manage_service.batch_append_products_to_promotions(
        shop_id=req.shop_id,
        platform_promotion_ids=req.platform_promotion_ids,
        platform_item_ids=req.platform_item_ids
    )
    return Result.success(data=res.get("report"))

@router.get("/list", response_model=Result[PromotionListRead])
async def get_promotion_list(
    shop_id: Optional[str] = Query(None, description="店铺 ID"),
    status: str = Query("", description="状态过滤"),
    title: str = Query("", description="活动标题模糊搜索"), 
    page_no: int = 1,
    page_size: int = 20
):
    """
    查询活动列表
    - 支持 shop_id 必填查询
    - 支持 status 和 title 可选过滤
    """
    res_data = manage_service.search_promotions(
        shop_ids=[shop_id], 
        status=status, 
        title=title, # 🎯 透传给 Service
        page_no=page_no, 
        page_size=page_size
    )
    return Result.success(data=res_data)

# =========================================================
# 2. 定价策略 (Strategy) CRUD
# =========================================================

@router.get("/strategy/list", response_model=Result[List[StrategySchema]])
async def list_strategies(shop_id: str, keyword: str = ""):
    strategies = price_dao.get_active_strategies(shop_id)
    if keyword:
        # 过滤包含关键词的策略
        strategies = [s for s in strategies if keyword.lower() in s.get("keyword", "").lower()]
    return Result.success(data=strategies)

@router.post("/strategy/save")
async def save_strategy(req: StrategySchema):
    price_dao.save_strategy(req.dict())
    return Result.success(msg="策略保存成功")

@router.delete("/strategy/delete")
async def delete_strategy(strategy_id: int):
    price_dao.delete_strategy(strategy_id)
    return Result.success(msg="策略已删除")

# =========================================================
# 3. SKU 覆盖 (Override) 与商品 SKU 搜索
# =========================================================

@router.get("/sku/search", response_model=Result[List[Dict]])
async def search_product_skus(shop_id: str, platform_item_id: str):
    """搜索具体商品的 SKU 列表，用于设置特价覆盖"""
    items = add_service._fetch_all_shop_items(shop_id, [platform_item_id], cookie=None)
    if items:
        # 兼容妙手不同的 SKU 返回字段
        skus = items[0].get("skus") or items[0].get("skuList") or []
        return Result.success(data=skus)
    return Result.fail(msg="未找到该商品的 SKU 数据")

@router.post("/sku-override/save")
async def save_sku_override(req: SkuOverrideSchema):
    price_dao.save_sku_override(
        sku_id=req.sku_id, 
        product_id=req.product_id, 
        shop_id=req.shop_id, 
        special_price=req.special_price
    )
    return Result.success(msg="SKU 特价保存成功")

@router.get("/sku-override/list", response_model=Result[List[SkuOverrideSchema]])
async def list_sku_overrides(shop_id: str):
    data = price_dao.get_all_overrides(shop_id)
    return Result.success(data=data)