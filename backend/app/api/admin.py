from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import require_roles
from app.schemas.lead import ChatMessageItem, LeadAssignUpdate, LeadItem, LeadStatusUpdate
from app.services.lead_service import LeadService
from app.services.user_service import UserService

router = APIRouter()
lead_service = LeadService()
user_service = UserService()
ALLOWED_STATUS = {"new", "contacted", "in_progress", "done"}


@router.get("/leads", response_model=list[LeadItem])
def list_leads(_: dict = Depends(require_roles("admin", "consultant", "operator"))) -> list[LeadItem]:
    return [LeadItem(**item) for item in lead_service.list_leads()]


@router.patch("/leads/{lead_id}/status")
def patch_lead_status(
    lead_id: int,
    payload: LeadStatusUpdate,
    _: dict = Depends(require_roles("admin", "consultant")),
) -> dict:
    if payload.status not in ALLOWED_STATUS:
        raise HTTPException(status_code=400, detail="invalid status")
    updated = lead_service.update_status(lead_id=lead_id, status=payload.status)
    if not updated:
        raise HTTPException(status_code=404, detail="lead not found")
    return {"ok": True}


@router.patch("/leads/{lead_id}/assign")
def patch_lead_assign(
    lead_id: int,
    payload: LeadAssignUpdate,
    _: dict = Depends(require_roles("admin", "consultant")),
) -> dict:
    updated = lead_service.assign_lead(lead_id=lead_id, assigned_to=payload.assigned_to)
    if not updated:
        raise HTTPException(status_code=404, detail="lead not found")
    return {"ok": True}


@router.get("/leads/{lead_id}/messages", response_model=list[ChatMessageItem])
def list_lead_messages(
    lead_id: int,
    _: dict = Depends(require_roles("admin", "consultant", "operator")),
) -> list[ChatMessageItem]:
    return [ChatMessageItem(**item) for item in lead_service.list_chat_messages(lead_id=lead_id)]


@router.get("/users")
def list_users(_: dict = Depends(require_roles("admin", "consultant", "operator"))) -> list[dict]:
    return user_service.list_users()
