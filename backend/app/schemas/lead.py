from pydantic import BaseModel


class LeadItem(BaseModel):
    id: int
    visitor_id: str
    first_message: str
    latest_message: str
    page_url: str | None
    status: str
    assigned_to: str | None = None
    notified_wechat: bool
    created_at: str
    updated_at: str


class LeadStatusUpdate(BaseModel):
    status: str


class LeadAssignUpdate(BaseModel):
    assigned_to: str


class ChatMessageItem(BaseModel):
    id: int
    lead_id: int
    visitor_id: str
    role: str
    message: str
    created_at: str
