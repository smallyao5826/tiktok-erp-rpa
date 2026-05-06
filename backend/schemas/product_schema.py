from pydantic import BaseModel, Field
from typing import List, Optional

class ProductSearchRequest(BaseModel):
    shop_ids: List[str] = Field(..., description="店铺 ID 列表")
    status: str = Field("onsale", description="商品状态：onsale, draft, deleted")
    platform_item_id: Optional[str] = Field(None, description="特定商品 ID")
    page_no: int = Field(1, ge=1)
    page_size: int = Field(20, ge=1, le=100)

# --- 单个商品清洗后的模型 ---
class ProductItemRead(BaseModel):
    platform_item_id: str
    title: str
    pic_url: Optional[str] = None  
    shop_id: str
    status: str

# --- 分页列表返回模型 ---
class ProductListRead(BaseModel):
    list: List[ProductItemRead]
    total: int
    page: int
    page_size: int