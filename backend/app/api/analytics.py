from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.schemas.analytics import AnalyticsSummaryResponse, AnalyticsTrackRequest
from app.services.analytics_service import AnalyticsService

router = APIRouter()
analytics_service = AnalyticsService()


@router.post("/track")
def track_event(payload: AnalyticsTrackRequest) -> dict:
    analytics_service.add_event(
        visitor_id=payload.visitor_id,
        event_type=payload.event_type,
        page_url=payload.page_url,
        payload=payload.payload,
    )
    return {"ok": True}


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def summary(_: dict = Depends(require_roles("admin", "consultant", "operator"))) -> AnalyticsSummaryResponse:
    return AnalyticsSummaryResponse(**analytics_service.summary())
