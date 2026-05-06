from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- 基础时间组件 ---
class TimeSlot(BaseModel):
    start: str = Field(..., example="2026-04-11 00:00:00")
    end: str = Field(..., example="2026-04-11 00:59:59")

# --- 1. 闪购活动操作请求 ---
class CreateFlashSaleRequest(BaseModel):
    shop_id: str
    time_slots: List[TimeSlot]
    platform_item_ids: Optional[List[str]] = None

class AddUpdateProductRequest(BaseModel):
    """添加或更新活动中的商品及价格"""
    shop_id: str
    platform_promotion_id: str
    product_list: List[Dict] 

class PromotionCopyRequest(BaseModel):
    """复制活动请求"""
    shop_id: str
    platform_promotion_id: str
    new_title: str
    new_start: str
    new_end: str

class BatchDeactivateRequest(BaseModel):
    """批量停用活动请求"""
    shop_id: str
    platform_promotion_ids: List[str]

class AppendProductsRequest(BaseModel):
    """批量追加商品到活动请求"""
    shop_id: str
    platform_promotion_ids: List[str]
    platform_item_ids: List[str]

class PromotionItemRead(BaseModel):
    """活动列表条目（二次封装版）"""
    platform_promotion_id: str
    title: str
    status: str
    gmt_local_begin: str
    gmt_local_end: str
    effective_item_count: int
    effective_sku_count: int
    add_fail_item_count: int

class PromotionListRead(BaseModel):
    """带分页的活动列表响应"""
    list: List[PromotionItemRead]
    total: int
    page: int
    page_size: int

# --- 2. 定价策略管理 (Strategy) ---
class StrategySchema(BaseModel):
    id: Optional[int] = None
    shop_id: str
    keyword: str
    rule_value: float
    rule_type: str  # 'fixed_price' 或 'discount_rate'
    priority: int = 0

# --- 3. SKU 覆盖管理 (Override) ---
class SkuOverrideSchema(BaseModel):
    sku_id: str
    product_id: str
    shop_id: str
    special_price: float