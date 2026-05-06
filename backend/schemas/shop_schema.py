from pydantic import BaseModel
from typing import List, Optional

class ShopBase(BaseModel):
    """店铺基础字段"""
    shop_id: str
    shop_nick: str
    site: str
    platform: Optional[str] = "TikTok"

class ShopRead(ShopBase):
    """用于返回给前端的格式"""
    # 如果以后有特殊的展示逻辑可以在这里扩展
    class Config:
        from_attributes = True  # 允许从类对象转换