from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    visitor_id: str = Field(..., description="Anonymous visitor id")
    message: str = Field(..., min_length=1, max_length=1500)
    page_url: str | None = None


class ChatResponse(BaseModel):
    reply: str
    notified_wechat: bool
    lead_id: int
