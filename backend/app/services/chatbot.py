import os

import httpx


class ChatbotService:
    """Use external LLM API when configured, fallback to rule-based reply."""

    def __init__(self) -> None:
        self.llm_api_url = os.getenv("LLM_API_URL", "").strip()
        self.llm_api_key = os.getenv("LLM_API_KEY", "").strip()
        self.llm_model = os.getenv("LLM_MODEL", "gpt-4o-mini").strip()

    async def reply(self, user_message: str) -> str:
        if self.llm_api_url and self.llm_api_key:
            llm_reply = await self._reply_from_llm(user_message)
            if llm_reply:
                return llm_reply
        return self._reply_from_rules(user_message)

    async def _reply_from_llm(self, user_message: str) -> str | None:
        payload = {
            "model": self.llm_model,
            "messages": [
                {
                    "role": "system",
                    "content": "你是申荣留学官网智能客服。请简洁、专业、友好，优先引导用户提供背景信息。",
                },
                {"role": "user", "content": user_message},
            ],
            "temperature": 0.4,
        }
        headers = {
            "Authorization": f"Bearer {self.llm_api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(self.llm_api_url, json=payload, headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return data["choices"][0]["message"]["content"].strip()
        except Exception:  # noqa: BLE001
            return None

    def _reply_from_rules(self, user_message: str) -> str:
        lower = user_message.lower()
        if "申请" in user_message or "study" in lower:
            return "您好，我可以先帮您做留学方向初步评估。请告诉我您的专业、GPA和目标国家。"
        if "费用" in user_message or "price" in lower:
            return "不同国家与服务内容费用不同，您可留下联系方式，顾问会为您提供详细方案。"
        if "雅思" in user_message or "toefl" in lower:
            return "语言成绩会影响学校选择。请告诉我当前成绩和目标院校层级，我帮您做建议。"
        return "已收到您的问题，我们的顾问会尽快联系您。您也可以继续告诉我更多背景信息。"
