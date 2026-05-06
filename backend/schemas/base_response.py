from pydantic import BaseModel
from typing import Optional, Any, TypeVar, Generic

T = TypeVar("T")

class Result(BaseModel, Generic[T]):
    """统一响应模型"""
    code: int = 200          # 状态码 (200: 成功, 400+: 业务失败, 500: 系统错误)
    msg: str = "success"     # 提示信息
    data: Optional[T] = None # 具体数据内容

    @classmethod
    def success(cls, data: Any = None, msg: str = "操作成功"):
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def fail(cls, msg: str = "操作失败", code: int = 400):
        return cls(code=code, msg=msg, data=None)