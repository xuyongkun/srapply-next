from pydantic import BaseModel, Field


class CaseCreateRequest(BaseModel):
    title: str = Field(..., min_length=2, max_length=120)
    summary: str = Field(..., min_length=5, max_length=1000)
    country: str = Field(..., min_length=2, max_length=50)
    major: str = Field(..., min_length=2, max_length=80)


class CaseItem(CaseCreateRequest):
    id: int
    created_at: str


class AdvisorCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=60)
    title: str = Field(..., min_length=2, max_length=80)
    bio: str = Field(..., min_length=5, max_length=1000)
    specialties: str = Field(..., min_length=2, max_length=200)


class AdvisorItem(AdvisorCreateRequest):
    id: int
    created_at: str
