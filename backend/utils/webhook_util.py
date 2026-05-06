import json
import aiohttp
import asyncio
import requests
import time
import hmac
import hashlib
import base64
from typing import Dict, Optional, Any, List
from utils.logger_util import get_logger

logger = get_logger("WebhookUtil")

class WebhookUtil:
    @staticmethod
    async def send_webhook_async(url: str, data: Dict[str, Any], timeout: int = 10) -> bool:
        """
        异步发送 Webhook 通知
        :param url: Webhook URL
        :param data: 发送的数据
        :param timeout: 超时时间（秒）
        :return: 是否发送成功
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    json=data,
                    headers={"Content-Type": "application/json"},
                    timeout=timeout
                ) as response:
                    if 200 <= response.status < 300:
                        logger.info(f"Webhook 发送成功: {url}")
                        return True
                    else:
                        logger.error(f"Webhook 发送失败，状态码: {response.status}, URL: {url}")
                        return False
        except Exception as e:
            logger.error(f"Webhook 发送异常: {str(e)}, URL: {url}")
            return False

    @staticmethod
    def send_webhook(url: str, data: Dict[str, Any], timeout: int = 10) -> bool:
        """
        同步发送 Webhook 通知
        :param url: Webhook URL
        :param data: 发送的数据
        :param timeout: 超时时间（秒）
        :return: 是否发送成功
        """
        try:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(
                WebhookUtil.send_webhook_async(url, data, timeout)
            )
        except Exception as e:
            logger.error(f"同步发送 Webhook 异常: {str(e)}")
            return False

    @staticmethod
    def send_webhook_batch(webhooks: list, data: Dict[str, Any], timeout: int = 10) -> list:
        """
        批量发送 Webhook 通知
        :param webhooks: Webhook 配置列表，每个元素包含 'url' 字段
        :param data: 发送的数据
        :param timeout: 超时时间（秒）
        :return: 发送结果列表，每个元素为 (url, 成功状态)
        """
        results = []
        for webhook in webhooks:
            url = webhook.get('url')
            if url:
                success = WebhookUtil.send_webhook(url, data, timeout)
                results.append((url, success))
        return results

class LarkUtil:
    def __init__(self, webhook_url: str, secret: str = None):
        """
        :param webhook_url: 飞书机器人的 Webhook 地址
        :param secret: 机器人的安全设置签名校验 (可选)
        """
        self.webhook_url = webhook_url
        self.secret = secret

    def _generate_signature(self, timestamp: int):
        """生成飞书签名校验"""
        string_to_sign = f"{timestamp}\n{self.secret}"
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()
        return base64.b64encode(hmac_code).decode("utf-8")

    def _send(self, payload: dict):
        """发送 POST 请求的核心方法"""
        try:
            if self.secret:
                timestamp = int(time.time())
                payload["timestamp"] = str(timestamp)
                payload["sign"] = self._generate_signature(timestamp)

            res = requests.post(self.webhook_url, json=payload, timeout=10)
            res.raise_for_status()
            result = res.json()
            
            if result.get("code") != 0:
                logger.error(f"飞书发送失败: {result.get('msg')}")
                return False
            return True
        except Exception as e:
            logger.exception(f"飞书 Webhook 请求异常: {str(e)}")
            return False

    def send_text(self, text: str):
        """发送简单的纯文本消息"""
        return self._send({
            "msg_type": "text",
            "content": {"text": text}
        })

    def send_summary_card(self, title: str, subtitle: str, fields: list, theme: str = "blue"):
        """
        发送高颜值的汇总统计卡片
        :param fields: 列表格式 [{"label": "字段名", "value": "内容"}]
        :param theme: 颜色主题: blue, green, orange, red, turquoise (青色)
        """
        # 1. 构造卡片头部
        card = {
            "header": {
                "title": {"tag": "plain_text", "content": title},
                "template": theme
            },
            "elements": [
                {
                    "tag": "div",
                    "text": {"tag": "lark_md", "content": f"**{subtitle}**"}
                },
                {"tag": "hr"} # 分割线
            ]
        }

        # 2. 构造多栏数据（两栏布局显示更精致）
        field_elements = []
        for f in fields:
            field_elements.append({
                "is_short": True,
                "text": {"tag": "lark_md", "content": f"**{f['label']}**\n{f['value']}"}
            })
        
        card["elements"].append({"tag": "div", "fields": field_elements})

        # 3. 构造底部脚注
        card["elements"].append({
            "tag": "note",
            "elements": [{"tag": "plain_text", "content": f"🚀 TikTok-MiaoShou RPA | {time.strftime('%Y-%m-%d %H:%M')}"}]
        })

        return self._send({
            "msg_type": "interactive",
            "card": card
        })
