from dao.webhook_dao import WebhookDao
from utils.logger_util import get_logger

logger = get_logger("SystemService")

class SystemService:
    def __init__(self):
        self.webhook_dao = WebhookDao()

    def get_webhook_configs(self):
        """
        获取所有Webhook配置
        """
        try:
            return self.webhook_dao.get_enabled_webhooks()
        except Exception as e:
            logger.error(f"获取Webhook配置失败: {str(e)}")
            return []

    def add_webhook(self, url):
        """
        添加Webhook配置
        """
        try:
            webhook_id = self.webhook_dao.add_webhook(url)
            logger.info(f"添加Webhook成功: {url}")
            return webhook_id
        except Exception as e:
            logger.error(f"添加Webhook失败: {str(e)}")
            return None

    def update_webhook(self, webhook_id, url=None, enabled=None):
        """
        更新Webhook配置
        """
        try:
            success = self.webhook_dao.update_webhook(webhook_id, url, enabled)
            if success:
                logger.info(f"更新Webhook成功: {webhook_id}")
            return success
        except Exception as e:
            logger.error(f"更新Webhook失败: {str(e)}")
            return False

    def delete_webhook(self, webhook_id):
        """
        删除Webhook配置
        """
        try:
            success = self.webhook_dao.delete_webhook(webhook_id)
            if success:
                logger.info(f"删除Webhook成功: {webhook_id}")
            return success
        except Exception as e:
            logger.error(f"删除Webhook失败: {str(e)}")
            return False
