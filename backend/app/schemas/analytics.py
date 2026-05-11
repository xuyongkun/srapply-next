from pydantic import BaseModel, Field


class AnalyticsTrackRequest(BaseModel):
    visitor_id: str = Field(..., min_length=1, max_length=80)
    event_type: str = Field(..., min_length=2, max_length=40)
    page_url: str | None = None
    payload: str | None = None


class AnalyticsTopPage(BaseModel):
    page_url: str | None
    hits: int


class AnalyticsSummaryResponse(BaseModel):
    total_visitors: int
    consultation_visitors: int
    conversion_rate: float
    top_pages: list[AnalyticsTopPage]
