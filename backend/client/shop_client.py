import time
from .base_client import BaseClient

class ShopClient(BaseClient):
    def __init__(self, headers=None):
        super().__init__(headers=headers)

    def get_shop_list(self, platform="tiktok", page_no=1, page_size=20, cookie_str=None):
        """
        获取店铺列表
        :param platform: 平台名称
        :param page_no: 页码
        :param page_size: 每页数量
        :param cookie_str: 手动传入的 Cookie 字符串
        """
        endpoint = "/api/auth/shop/getShopList"
        
        # 构造请求体 (application/x-www-form-urlencoded)
        data = {
            "platform": platform,
            "site": "",
            "keyword": "",
            "isCnsc": "",
            "onlyReauthorization": 0,
            "isAuthInvalid": "",
            "pageSize": page_size,
            "pageNo": page_no
        }

        # 构造 Header (完全参照 curl 日志)
        timestamp = str(int(time.time()))
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Breadcrumb": "auth-authShop-shopee",
            "bx-v": "2.5.11",
            "x-app-rhino": "1f8628bbc259bafd45850a5585c3d11a", # 动态签名，若失效需更新
            "x-front-version": "1775714523704",
            "x-timestamp": timestamp,
            "Origin": "https://erp.91miaoshou.com",
            "Referer": "https://erp.91miaoshou.com/auth_shop/index"
        }

        if cookie_str:
            headers["Cookie"] = cookie_str

        # 发送请求
        return self.post(endpoint, data=data, headers=headers, cookie_str=cookie_str)