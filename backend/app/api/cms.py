from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.schemas.cms import AdvisorCreateRequest, AdvisorItem, CaseCreateRequest, CaseItem
from app.services.cms_service import CmsService

router = APIRouter()
cms_service = CmsService()


@router.get("/cases", response_model=list[CaseItem])
def list_cases() -> list[CaseItem]:
    return [CaseItem(**item) for item in cms_service.list_cases()]


@router.post("/cases", response_model=CaseItem)
def create_case(
    payload: CaseCreateRequest,
    _: dict = Depends(require_roles("admin", "consultant")),
) -> CaseItem:
    case_id = cms_service.create_case(
        title=payload.title,
        summary=payload.summary,
        country=payload.country,
        major=payload.major,
    )
    case = next(item for item in cms_service.list_cases() if item["id"] == case_id)
    return CaseItem(**case)


@router.get("/advisors", response_model=list[AdvisorItem])
def list_advisors() -> list[AdvisorItem]:
    return [AdvisorItem(**item) for item in cms_service.list_advisors()]


@router.post("/advisors", response_model=AdvisorItem)
def create_advisor(
    payload: AdvisorCreateRequest,
    _: dict = Depends(require_roles("admin", "consultant")),
) -> AdvisorItem:
    advisor_id = cms_service.create_advisor(
        name=payload.name,
        title=payload.title,
        bio=payload.bio,
        specialties=payload.specialties,
    )
    advisor = next(item for item in cms_service.list_advisors() if item["id"] == advisor_id)
    return AdvisorItem(**advisor)
