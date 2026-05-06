import base64
import time
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from .base_client import BaseClient

class AuthClient(BaseClient):
    def __init__(self, headers=None):
        super().__init__(headers=headers)
        self.aes_key = "@3438jj;siduf832"

    def _aes_encrypt(self, text: str) -> str:
        key = self.aes_key.encode('utf-8')
        iv = b'\x00' * 16
        cipher = AES.new(key, AES.MODE_CBC, iv)
        padded_data = pad(text.encode('utf-8'), AES.block_size)
        return base64.b64encode(cipher.encrypt(padded_data)).decode('utf-8')

    def get_captcha_data(self):
        endpoint = "/api/auth/account/getCaptcha"
        res = self.get(endpoint)
        if res.get("result") == "success":
            uuid = res.get("captchaUuid")
            img_b64 = res.get("captchaUri").split(",")[-1]
            return uuid, base64.b64decode(img_b64)
        return None, None

    def login(self, mobile_raw, password_raw, captcha_code, captcha_uuid):
        endpoint = "/api/auth/account/login"
        data = {
            "mobile": self._aes_encrypt(mobile_raw),
            "password": self._aes_encrypt(password_raw),
            "captcha": captcha_code,
            "captchaUuid": captcha_uuid,
            "isWhitelistIp": 0,
            "isVerifyRemoteLogin": "true"
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "X-BreadCrumb": "system-login"}
        return self.post(endpoint, data=data, headers=headers)

    def get_account_info(self, timestamp=None, cookie_str=None):
        endpoint = "/api/auth/account/getAccountInfo"
        headers = {
            "bx-v": "2.5.11",
            "x-app-zebra": "92cd04deadf067dc300209ed1b27e980",
            "x-front-version": "1775704039448",
            "x-timestamp": str(timestamp or int(time.time()))
        }
        return self.get(endpoint, headers=headers, cookie_str=cookie_str)