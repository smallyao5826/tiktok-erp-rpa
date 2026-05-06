import time
import json
from .base_client import BaseClient

class PromotionClient(BaseClient):
    def __init__(self, headers=None):
        super().__init__(headers=headers)

    # --- 同步全店促销 ---
    def rsync_full_shop_promotion(self, shop_ids, cookie_str=None):
        endpoint = "/api/platform/tiktok/item/promotion/rsyncFullShopPromotion"
        shop_ids_str = ",".join(shop_ids) if isinstance(shop_ids, list) else str(shop_ids)
        data = {"shopIds": shop_ids_str}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "56e45d23f2884f010ebed1641f36d073",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    # --- 查询待参加促销商品 ---
    def search_wait_add_promotion_item_list(self, shop_id, page_no=1, page_size=20, product_type=2, platform_promotion_id="", cookie_str=None):
        endpoint = "/api/platform/tiktok/item/promotion/searchWaitAddPromotionItemList"
        data = {
            "shopId": str(shop_id), "pageNo": page_no, "pageSize": page_size,
            "platformPromotionId": platform_promotion_id, "productType": product_type
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "4c7fb54ce2d82e4f31bedaf4d2c881e0",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale/create"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    # --- 创建促销活动任务 ---
    def add_multi_shop_promotion(self, shop_ids, title, begin_time, end_time, product_type=2, promotion_type=3, cookie_str=None):
        endpoint = "/api/platform/tiktok/item/promotion/addMultiShopPromotion"
        data = {
            "promotionInfo[title]": title, "promotionInfo[productType]": product_type,
            "promotionInfo[promotionType]": promotion_type, "promotionInfo[gmtLocalBegin]": begin_time,
            "promotionInfo[gmtLocalEnd]": end_time, "autoExtensionInfo[isAutoExtension]": 0,
            "autoExtensionInfo[cycle]": 3, "autoExtensionInfo[isHighPriority]": 0
        }
        for i, sid in enumerate(shop_ids):
            data[f"shopIds[{i}]"] = sid
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "339d178d0d9a89b062a6bcf42e88bc22",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale/create"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    # --- 添加/更新折扣商品 ---
    def add_or_update_promotion_discount_products(self, shop_id, platform_promotion_id, product_list, cookie_str=None):
        endpoint = "/api/platform/tiktok/item/promotion/addOrUpdatePromotionDiscountProducts"
        data = {
            "shopId": str(shop_id), "platformPromotionId": str(platform_promotion_id),
            "productList": json.dumps(product_list)
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "1de94c54be299dc182590f6f01fa5b02",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale/create"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    # --- 复制活动 ---
    def copy_promotion(self, promotion_data, cookie_str=None):
        """
        复制活动
        :param promotion_data: 包含活动详情的字典（通常从 searchPromotionList 获取）
        """
        endpoint = "/api/platform/tiktok/item/promotion/copyPromotion"
        # 复制接口通常直接发送原活动的所有字段
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "fac3d16777cde975cdd23f36ae17fb02",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale"
        }
        # 将 autoExtensionInfo 内部字典平铺为表单格式
        if "autoExtensionInfo" in promotion_data:
            info = promotion_data.pop("autoExtensionInfo")
            promotion_data["autoExtensionInfo[isAutoExtension]"] = info.get("isAutoExtension", 0)

        return self.post(endpoint, data=promotion_data, headers=headers, cookie_str=cookie_str)

    # --- 停用（结束）活动 ---
    def deactivate_promotion(self, shop_id, platform_promotion_id, cookie_str=None):
        """
        结束/停用指定的促销活动
        """
        endpoint = "/api/platform/tiktok/item/promotion/deactivatePromotion"
        data = {
            "promotionList[0][shopId]": str(shop_id),
            "promotionList[0][platformPromotionId]": str(platform_promotion_id)
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "47e437006176522111f98553318d6cd4",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    # --- 查询促销活动列表 ---
    def search_promotion_list(self, shop_ids=None, status="", title="", page_no=1, page_size=20, erp_promotion_type="flashSale", cookie_str=None):
        """
        获取已创建的活动列表
        :param shop_ids: 店铺 ID 列表，如 ["13521974"]
        :param status: 状态 (1: 未开始, 2: 进行中, 3: 已过期, 4: 已停用)
        """
        endpoint = "/api/platform/tiktok/item/promotion/searchPromotionList"
        data = {
            "status": status,
            "title": title,
            "erpPromotionType": erp_promotion_type,
            "pageNo": page_no,
            "pageSize": page_size
        }
        
        # 如果传入了店铺 ID 列表，按照 shopIds[0] 格式注入
        if shop_ids:
            for i, sid in enumerate(shop_ids):
                data[f"shopIds[{i}]"] = sid

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "16bed22fcb3a32222e0357af82535c4d",
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)

    # --- 重试添加商品 ---
    def retry_add_promotion_items(self, shop_id, platform_promotion_id, platform_item_ids, cookie_str=None):
        """
        针对添加失败的商品进行重试
        :param shop_id: 店铺 ID
        :param platform_promotion_id: 活动 ID
        :param platform_item_ids: 需要重试的平台商品 ID 列表
        """
        endpoint = "/api/platform/tiktok/item/promotion/retryAddPromotionItems"
        data = {
            "shopId": str(shop_id),
            "platformPromotionId": str(platform_promotion_id)
        }
        # 按照 platformItemIds[0]=xxx 格式构造
        for i, pid in enumerate(platform_item_ids):
            data[f"platformItemIds[{i}]"] = str(pid)

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "x-app-rhino": "82c1ebf1699963ae6f6edcf8be0a4bbe", # 该接口特有的 rhino
            "x-front-version": "1775716844881",
            "x-timestamp": str(int(time.time())),
            "Referer": "https://erp.91miaoshou.com/tiktok/marketing/flashSale"
        }
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)