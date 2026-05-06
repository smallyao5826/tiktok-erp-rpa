from .base_dao import BaseDao
from typing import List, Dict, Optional

class WebhookDao(BaseDao):
    def get_enabled_webhooks(self) -> List[Dict]:
        """
        获取所有启用的 Webhook 配置
        :return: Webhook 配置列表
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, url FROM webhook_configs WHERE enabled = 1")
            
            webhooks = []
            for row in cursor.fetchall():
                webhooks.append({
                    'id': row[0],
                    'url': row[1]
                })
            return webhooks

    def add_webhook(self, url: str) -> int:
        """
        添加新的 Webhook 配置
        :param url: Webhook URL
        :return: 新添加的 Webhook ID
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO webhook_configs (url) VALUES (?) ",
                (url,)
            )
            conn.commit()
            return cursor.lastrowid

    def update_webhook(self, webhook_id: int, url: Optional[str] = None, enabled: Optional[bool] = None) -> bool:
        """
        更新 Webhook 配置
        :param webhook_id: Webhook ID
        :param url: 新的 URL（可选）
        :param enabled: 是否启用（可选）
        :return: 是否更新成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # 构建更新语句
            update_fields = []
            params = []
            
            if url is not None:
                update_fields.append("url = ?")
                params.append(url)
            if enabled is not None:
                update_fields.append("enabled = ?")
                params.append(1 if enabled else 0)
            
            if not update_fields:
                return False
            
            params.append(webhook_id)
            query = f"UPDATE webhook_configs SET {', '.join(update_fields)} WHERE id = ?"
            
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0

    def delete_webhook(self, webhook_id: int) -> bool:
        """
        删除 Webhook 配置
        :param webhook_id: Webhook ID
        :return: 是否删除成功
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM webhook_configs WHERE id = ?", (webhook_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_webhook_by_id(self, webhook_id: int) -> Optional[Dict]:
        """
        根据 ID 获取 Webhook 配置
        :param webhook_id: Webhook ID
        :return: Webhook 配置字典，如果不存在则返回 None
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, url, enabled, event_type, created_at FROM webhook_configs WHERE id = ?", (webhook_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'url': row[1],
                    'enabled': bool(row[2]),
                    'event_type': row[3],
                    'created_at': row[4]
                }
            return None
