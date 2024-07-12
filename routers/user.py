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

verification_codes = {}


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

    code = ''.join(random.choices(string.digits, k=6))

    verification_codes[request.user_id] = {
        "code": code,
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
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

    verification_data = verification_codes.get(request.user_id)
    if not verification_data or verification_data["code"] != request.verification_code:
        raise HTTPException(status_code=400, detail="Invalid or expired verification code")

    if verification_data["expires_at"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Verification code has expired")

    del verification_codes[request.user_id]

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
