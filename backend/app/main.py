import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin, analytics, auth, chat, cms, public, webhook


app = FastAPI(
    title="Shenrong New Website API",
    description="Public website, admin, AI chat and WeChat notification APIs.",
    version="0.1.0",
)

cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173")
allow_origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(public.router, prefix="/api/public", tags=["public"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(webhook.router, prefix="/api/wechat", tags=["wechat"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(cms.router, prefix="/api/cms", tags=["cms"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
