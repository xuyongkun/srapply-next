from fastapi import APIRouter, HTTPException

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.analytics_service import AnalyticsService
from app.services.chatbot import ChatbotService
from app.services.lead_service import LeadService
from app.services.wechat_notifier import WechatNotifier

router = APIRouter()
chatbot = ChatbotService()
wechat = WechatNotifier()
lead_service = LeadService()
analytics_service = AnalyticsService()


@router.post("/visitor", response_model=ChatResponse)
async def visitor_chat(payload: ChatRequest) -> ChatResponse:
    try:
        reply = await chatbot.reply(payload.message)
        notified = await wechat.send_visitor_message(payload.visitor_id, payload.message, payload.page_url)
        lead_id = lead_service.upsert_from_chat(
            visitor_id=payload.visitor_id,
            message=payload.message,
            page_url=payload.page_url,
            notified_wechat=notified,
        )
        lead_service.add_chat_message(lead_id=lead_id, visitor_id=payload.visitor_id, role="bot", message=reply)
        analytics_service.add_event(
            visitor_id=payload.visitor_id,
            event_type="chat_submit",
            page_url=payload.page_url,
            payload=payload.message[:200],
        )
        return ChatResponse(reply=reply, notified_wechat=notified, lead_id=lead_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"chat service failed: {exc}") from exc
