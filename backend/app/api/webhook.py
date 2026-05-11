from fastapi import APIRouter

router = APIRouter()


@router.post("/event")
async def receive_wechat_event(payload: dict) -> dict:
    """Reserved endpoint for future WeChat callbacks."""
    return {"received": True, "payload": payload}
