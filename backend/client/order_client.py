import time
from .base_client import BaseClient

class OrderClient(BaseClient):
    def __init__(self, headers=None):
        super().__init__(headers=headers)

    def search_order_package_list(
        self, 
        shop_ids=None, 
        page_no=1, 
        page_size=10, 
        start_time=None,  
        end_time=None,    
        tab="waitShip", 
        cookie_str=None
    ):
        endpoint = "/api/order/new_package/searchOrderPackageList"
        
        # 1. 构造 Payload (补全了 curl 中存在的默认字段，确保后端逻辑闭环)
        data = {
            "pageSize": page_size,
            "page": page_no,
            "goodsSkuOuterIdRp": "ss",
            "platformOuterSkuIdRp": "ss",
            "purchaseLogisticsKeywordRp": "eq",
            "logisticsKeywordRp": "eq",
            "platformOrderSnsRp": "eq",
            "appPackageNosRp": "eq",
            "appPackageNos": "",
            "purchaseOrderSnRp": "eq",
            "platformItemNumRp": "eq",
            "warehouseShelfCellCodeRp": "ss",
            "priceType": "profit",
            "remarkRp": "ss",
            "skuSubNameRp": "ss",
            "packageWeighingWeightRp": "g",
            "itemTitleRp": "ss",
            "consigneeZipCodeRp": "ss",
            "sourceItemIdsRp": "eq",
            "platformOrderSns": "",
            "gmtLastDeliveryFrom": "",
            "gmtLastDeliveryTo": "",
            "orderTagsRp": "includeAll",
            "logisticsGroupType": "cascader",
            "source": "orderProcess",
            "appPackageTab": tab,
            "sortField": "gmtOrderStart",
            "sortType": "desc",
            "waitProcessTab": "all",
            "supplierProcessStatus": "all",
            "isLogisticsCompanyGroupMode": 1
        }
        
        if start_time: data["gmtOrderStartFrom"] = start_time
        if end_time: data["gmtOrderStartTo"] = end_time

        if shop_ids:
            if isinstance(shop_ids, list):
                for i, sid in enumerate(shop_ids):
                    data[f"shopIds[{i}]"] = str(sid)
            else:
                data["shopIds[0]"] = str(shop_ids)

        # 2. 🎯 核心修改：根据最新 curl 同步 Header
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json, text/plain, */*",
            # 关键：从 x-app-hippo 更改为 x-app-zebra
            "x-app-zebra": "c8ad7486540d5e68a4429626c006bce3", 
            "x-front-version": "1775804115607", # 同步 curl 中的版本
            "x-timestamp": str(int(time.time())),
            "bx-v": "2.5.11",
            "Origin": "https://erp.91miaoshou.com",
            "Referer": f"https://erp.91miaoshou.com/order/package/index?appPackageTab={tab}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"
        }

        if cookie_str:
            headers["Cookie"] = cookie_str

        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)