import time
import base64
from client.auth_client import AuthClient
from dao.auth_dao import AuthDao  # 切换到新的 DAO
from utils.logger_util import get_logger
from utils.ocr_util import ocr_tool

logger = get_logger("AuthService")

class AuthService:
    def __init__(self):
        self.client = AuthClient()
        self.dao = AuthDao()  # 使用专门的账号管家
        self.max_ocr_retries = 3

    def login_and_save(self, account, password):
        """
        外部调用接口：传入账号密码，全自动完成识别、登录和存储
        """
        return self._auto_login_logic(account, password)

    def _auto_login_logic(self, account, password):
        for i in range(self.max_ocr_retries):
            uuid, img_bytes = self.client.get_captcha_data()
            if not uuid: continue

            captcha_code = ocr_tool.recognize(img_bytes)
            logger.info(f"[*] 第 {i+1} 次尝试登录，OCR识别验证码: {captcha_code}")

            res = self.client.login(account, password, captcha_code, uuid)
            
            if res.get("result") == "success":
                cookie_dict = self.client.session.cookies.get_dict()
                cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
                
                # 🎯 调用 DAO 存储，Service 不再手写 SQL
                self.dao.save_profile(account, password, cookie_str)
                logger.info(f"[√] 账户 {account} 自动登录成功")
                return {"status": "success", "cookie": cookie_str}
            
            reason = res.get("reason", "")
            if "验证码" in reason:
                time.sleep(1)
                continue
            else:
                return {"status": "fail", "reason": reason}
        return {"status": "fail", "reason": "验证码重试过多"}

    def get_valid_cookie(self):
        # 🎯 从 DAO 获取 profile
        profile = self.dao.get_profile()
        if not profile:
            logger.warning("数据库无登录记录")
            return None
        
        account, password, old_cookie = profile['account'], profile['password'], profile['cookie']

        info = self.client.get_account_info(cookie_str=old_cookie)
        if info.get("result") == "success":
            return old_cookie
        
        # 失效则触发自动重登
        login_res = self._auto_login_logic(account, password)
        return login_res.get("cookie") if login_res.get("status") == "success" else None

    def get_account_info(self):
        """获取当前账户信息"""
        # 获取有效的cookie
        cookie = self.get_valid_cookie()
        if not cookie:
            return None
        
        # 使用cookie获取账户信息
        info = self.client.get_account_info(cookie_str=cookie)
        if info.get("result") == "success":
            return info
        return None