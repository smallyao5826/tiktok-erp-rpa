from typing import Dict, Optional, List
from client.shop_client import ShopClient
from utils.logger_util import get_logger
from utils.decorators import require_auth

logger = get_logger("ShopService")

class ShopService:
    def __init__(self):
        self.client = ShopClient()
        
    @require_auth
    def get_all_shops(self, cookie_str: str = None) -> List[Dict]:
        try:
            res = self.client.get_shop_list(page_size=100, cookie_str=cookie_str)
            
            if res.get("result") != "success":
                logger.error(f"获取店铺列表失败: {res.get('reason')}")
                return []

            raw_list = res.get("shopList", []) or res.get("list", [])
            cleaned_list = []
            for s in raw_list:
                # 🎯 关键修改：这里的 Key 必须和 ShopRead Schema 里的属性名一模一样
                cleaned_list.append({
                    "shop_id": str(s.get("shopId")),      # 以前是 shopId
                    "shop_nick": s.get("shopNick"),     # 以前是 shopNick
                    "site": s.get("site", "").upper(),
                    "platform": s.get("platformName", "TikTok")
                })
            
            logger.info(f"[√] 成功获取 {len(cleaned_list)} 个店铺")
            return cleaned_list

        except Exception as e:
            logger.exception(f"获取全部店铺异常: {str(e)}")
            return []

    def get_shop_info(self, target_id: str, cookie_str: str = None) -> Optional[Dict]:
        # 1. 拿到清洗后的店铺列表
        shops = self.get_all_shops(cookie_str=cookie_str)
        target_id_str = str(target_id)
        
        for shop in shops:
            if str(shop.get("shop_id")) == target_id_str:
                return {
                    "shopId": shop.get("shop_id"),      # 内部逻辑如果依赖驼峰，可以这里转回去
                    "shopNick": shop.get("shop_nick"),
                    "site": shop.get("site"),
                    "platformName": shop.get("platform")
                }
        return None