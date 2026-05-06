import time
import json
from .base_client import BaseClient

class ProductClient(BaseClient):
    def __init__(self, headers=None):
        super().__init__(headers=headers)

    def search_item_list(self, shop_ids, status="onsale", page_no=1, page_size=20, platform_item_id=None, cookie_str=None):
        """
        搜索/查询商品列表
        :param platform_item_id: 支持单个或多个 ID（逗号分隔），例如 "ID1,ID2"
        """
        endpoint = "/api/platform/tiktok/item/item/searchItemList"
        
        data = {
            "status": status,
            "publishShopStatus": "published",
            "titleType": "multi",
            "pageSize": page_size,
            "pageNo": page_no,
            "skuNumRp": "eq"
        }

        # 🎯 核心逻辑：支持多 ID 搜索
        if platform_item_id:
            # 1. 将中文逗号替换为英文逗号
            # 2. 去除所有空格，确保 ERP 接口识别准确
            clean_ids = str(platform_item_id).replace("，", ",").replace(" ", "")
            data["platformItemId"] = clean_ids
        
        for i, sid in enumerate(shop_ids):
            data[f"shopId[{i}]"] = sid

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Breadcrumb": "item-tiktok-item",
            "bx-v": "2.5.11",
            "x-app-rhino": "6c9d2c5f472c411ad63a5ca132d57167", # 对应 searchItemList 的签名
            "x-front-version": "1775714523704",
            "x-timestamp": str(int(time.time())),
            "Referer": "https://erp.91miaoshou.com/tiktok/item/item"
        }

        if cookie_str:
            headers["Cookie"] = cookie_str

        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    def rsync_item_batch(self, shop_id, platform_item_ids, cookie_str=None):
        """
        批量同步多个商品数据
        :param shop_id: 店铺 ID
        :param platform_item_ids: 平台商品 ID 列表，例如 ["id1", "id2"]
        """
        endpoint = "/api/item/item/rsyncItemBatch"
        
        # 核心改动：循环生成多个商品对象
        sync_data = [
            {
                "shopId": str(shop_id),
                "platformItemId": str(pid)
            } for pid in platform_item_ids
        ]
        
        data = {
            "shopIdAndPlatformItemIdJson": json.dumps(sync_data)
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Breadcrumb": "item-tiktok-item",
            "bx-v": "2.5.11",
            "x-app-rhino": "b5ffdb5dca66d36427d413f1a2ddf6b1", 
            "x-front-version": "1775716844881",
            "x-timestamp": str(int(time.time())),
            "Origin": "https://erp.91miaoshou.com",
            "Referer": "https://erp.91miaoshou.com/tiktok/item/item"
        }

        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)