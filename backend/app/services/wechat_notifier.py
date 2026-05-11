import os

import httpx


class WechatNotifier:
    """Send visitor chat events to WeChat customer service webhook."""

    def __init__(self) -> None:
        self.webhook_url = os.getenv("WECHAT_WEBHOOK_URL", "").strip()

    async def send_visitor_message(self, visitor_id: str, message: str, page_url: str | None) -> bool:
        if not self.webhook_url:
            return False

        content = (
            "【官网访客咨询】\n"
            f"访客ID: {visitor_id}\n"
            f"页面: {page_url or 'unknown'}\n"
            f"消息: {message}"
        )

        payload = {"msgtype": "text", "text": {"content": content}}

        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.post(self.webhook_url, json=payload)
            resp.raise_for_status()
        return True
