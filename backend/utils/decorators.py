import functools
from service.auth_service.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

auth_service = AuthService()

def require_auth(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 1. 检查调用者是否已经手动传入了 cookie_str
        manual_cookie = kwargs.get('cookie_str')
        
        if manual_cookie:
            # 如果手动传了，直接放行，不再去查数据库或 OCR 识别
            logger.info("[*] 检测到手动传入 Cookie，跳过自动认证流程")
            return func(*args, **kwargs)
        
        # 2. 如果没传，执行原有的全自动获取逻辑
        cookie = auth_service.get_valid_cookie()
        if not cookie:
            raise Exception("登录失效且自动识别验证码失败，请检查账号状态")
            
        kwargs['cookie_str'] = cookie 
        return func(*args, **kwargs)
    
    return wrapper