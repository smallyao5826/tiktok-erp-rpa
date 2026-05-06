from typing import List, Dict
from client.product_client import ProductClient
from utils.logger_util import get_logger
from utils.decorators import require_auth

logger = get_logger("ProductService")

class ProductService:
    def __init__(self):
        self.client = ProductClient()

    @require_auth
    def search_products(
        self, 
        shop_ids: List[str], 
        status: str = "onsale", 
        page_no: int = 1, 
        page_size: int = 20, 
        platform_item_id: str = None, 
        cookie_str: str = None
    ) -> Dict:
        try:
            res = self.client.search_item_list(
                shop_ids=shop_ids,
                status=status,
                page_no=page_no,
                page_size=page_size,
                platform_item_id=platform_item_id, 
                cookie_str=cookie_str
            )

            if res.get("result") != "success":
                logger.error(f"查询商品列表失败: {res.get('reason')}")
                return {"list": [], "total": 0, "page": page_no, "page_size": page_size}

            raw_list = res.get("itemList", []) or []
            cleaned_list = []

            for item in raw_list:
                # 计算 SKU 数量
                skus = item.get("skuList", []) or []
                
                cleaned_list.append({
                    "platform_item_id": str(item.get("platformItemId")),
                    "title": item.get("title"),
                    "pic_url": item.get("picUrl"), 
                    "shop_id": str(item.get("shopId")),
                    "status": item.get("status"),
                })

            return {
                "list": cleaned_list,
                "total": res.get("total", 0),
                "page": int(res.get("pageNo", page_no)),
                "page_size": int(res.get("pageSize", page_size))
            }

        except Exception as e:
            logger.exception(f"ProductService 运行异常: {str(e)}")
            return {"list": [], "total": 0, "page": page_no, "page_size": page_size}

    @require_auth
    def get_onsale_count(self, shop_id: str, cookie_str: str = None) -> int:
        """
        获取指定店铺在售商品的总数
        """
        try:
            res = self.client.search_item_list(
                shop_ids=[shop_id],
                status="onsale",
                page_no=1,
                page_size=1,
                cookie_str=cookie_str
            )

            if res.get("result") == "success":
                return int(res.get("total", 0))
            
            logger.error(f"获取在售数量失败: {res.get('reason')}")
            return 0

        except Exception as e:
            logger.exception(f"ProductService.get_onsale_count 运行异常: {str(e)}")
            return 0