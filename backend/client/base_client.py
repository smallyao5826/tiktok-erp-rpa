import requests

class BaseClient:
    def __init__(self, base_url="https://erp.91miaoshou.com", headers=None):
        self.base_url = base_url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
            "Accept": "application/json, text/plain, */*"
        }
        self.session = requests.Session()

    def _handle_headers(self, custom_headers, cookie_str):
        """统一处理 Header 合并和 Cookie 注入"""
        headers = {**self.headers, **(custom_headers or {})}
        if cookie_str:
            headers["Cookie"] = cookie_str
        return headers
    
    def get(self, endpoint, params=None, cookie_str=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        # 现在这里能找到 cookie_str 了
        headers = self._handle_headers(kwargs.get('headers'), cookie_str)
        response = self.session.get(url, params=params, headers=headers)
        return response.json()
    
    def post(self, endpoint, data=None, json=None, cookie_str=None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        # 现在这里能找到 cookie_str 了
        headers = self._handle_headers(kwargs.get('headers'), cookie_str)
        response = self.session.post(url, data=data, json=json, headers=headers)
        return response.json()