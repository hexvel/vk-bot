import random
import string
from fastapi import APIRouter, HTTPException
from models.user import Users
from config import Config, Emoji
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/api/users",
)

verification_data = {}


class VerificationCodeRequest(BaseModel):
    user_id: int


class TokenUpdateRequest(BaseModel):
    user_id: int
    token: str
    verification_code: str


@router.get("")
async def get_user_by_id(user_id: int):
    data = await Users.filter(user_id=user_id).first()

    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "status": "ok",
        "user": data
    }


@router.post("/request-verification-code")
async def request_verification_code(request: VerificationCodeRequest):
    data = await Users.filter(user_id=request.user_id).first()

    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    now = datetime.utcnow()
    user_data = verification_data.get(request.user_id)
    if user_data and 'last_request' in user_data:
        time_since_last_request = now - user_data['last_request']
        if time_since_last_request < timedelta(minutes=1):
            raise HTTPException(status_code=429, detail="Too many requests. Please wait before requesting a new code.")

    code = ''.join(random.choices(string.digits, k=6))

    verification_data[request.user_id] = {
        "code": code,
        "expires_at": now + timedelta(minutes=10),
        "last_request": now
    }

    await Config.GROUP[214167102].api.messages.send(
        user_id=request.user_id,
        message=f"{Emoji.SETTINGS} Ваш код подтверждения: {code}",
        random_id=0
    )

    return {
        "status": "ok",
        "message": "Verification code sent"
    }


@router.patch("/token")
async def update_token(request: TokenUpdateRequest):
    data = await Users.filter(user_id=request.user_id).first()

    if not data:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = verification_data.get(request.user_id)
    if not user_data or user_data["code"] != request.verification_code:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    if user_data["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code has expired")

    del verification_data[request.user_id]

    data.token = request.token
    await data.save()

    await Config.GROUP[214167102].api.messages.send(
        user_id=request.user_id,
        message=f"{Emoji.SETTINGS} Ваш токен изменён через "
                f"панель админа\nПожалуйста, перезагрузите "
                f"модуль.",
        random_id=0
    )

    return {
        "status": "ok",
        "user": data,
    }
