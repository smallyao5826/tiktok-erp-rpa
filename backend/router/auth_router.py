from fastapi import APIRouter, Depends, Body
from schemas.base_response import Result
from schemas.auth_schema import LoginRequest
from service.auth_service.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["认证管理"])

# 建议在外部初始化，或者使用依赖注入
auth_service = AuthService()

@router.post("/login", response_model=Result[str])
async def login(req: LoginRequest):
    """
    全自动 OCR 登录接口
    """
    # 调用你刚才写的 Service 逻辑
    res = auth_service.login_and_save(req.account, req.password)
    
    if res.get("status") == "success":
        # 返回成功体，data 存放 cookie
        return Result.success(data=res.get("cookie"), msg="登录并存储成功")
    else:
        # 返回失败体
        return Result.fail(msg=res.get("reason", "登录失败"))

@router.get("/cookie", response_model=Result[str])
async def get_cookie():
    """
    获取当前数据库中有效的 Cookie
    """
    cookie = auth_service.get_valid_cookie()
    if cookie:
        return Result.success(data=cookie)
    return Result.fail(msg="未找到可用登录记录，请先登录", code=401)

@router.get("/account/info", response_model=Result[dict])
async def get_account_info():
    """
    获取当前账户信息
    """
    info = auth_service.get_account_info()
    if info:
        # 提取账户信息，确保不包含密码等敏感信息
        account_data = {
            "account": info.get("accountName", "")
        }
        return Result.success(data=account_data)
    return Result.fail(msg="未找到可用登录记录，请先登录", code=401)