from fastapi import APIRouter, Body
from schemas.base_response import Result
from service.system_service.system_service import SystemService

router = APIRouter(prefix="/api/system", tags=["系统配置管理"])
system_service = SystemService()

@router.get("/webhook/list", response_model=Result[list])
async def get_webhook_list():
    """
    获取所有Webhook配置
    """
    webhooks = system_service.get_webhook_configs()
    return Result.success(data=webhooks)

@router.post("/webhook/add", response_model=Result[dict])
async def add_webhook(url: str = Body(..., description="Webhook URL")):
    """
    添加Webhook配置
    """
    webhook_id = system_service.add_webhook(url)
    if webhook_id:
        return Result.success(data={"webhook_id": webhook_id}, msg="Webhook添加成功")
    return Result.fail(msg="Webhook添加失败")

@router.post("/webhook/update", response_model=Result[dict])
async def update_webhook(
    webhook_id: int = Body(..., description="Webhook ID"),
    url: str = Body(None, description="Webhook URL"),
    enabled: bool = Body(None, description="是否启用")
):
    """
    更新Webhook配置
    """
    success = system_service.update_webhook(webhook_id, url, enabled)
    if success:
        return Result.success(msg="Webhook更新成功")
    return Result.fail(msg="Webhook更新失败")

@router.post("/webhook/delete", response_model=Result[dict])
async def delete_webhook(webhook_id: int = Body(..., description="Webhook ID")):
    """
    删除Webhook配置
    """
    success = system_service.delete_webhook(webhook_id)
    if success:
        return Result.success(msg="Webhook删除成功")
    return Result.fail(msg="Webhook删除失败")
