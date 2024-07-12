from vkbottle.user import Message, UserLabeler

from config import Config, Emoji
from models.user import Users
from services.rules.id import FindID
from services.rules.scope import Scope
from utils.helpers import check_token, search_text

labeler = UserLabeler()


@labeler.message(Scope(prefix=".й", commands=["рег"], rank=2), FindID())
async def registration(message: Message, user_id: int):
    user = await Users.filter(user_id=user_id).first()

    if user:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.NO} Пользователь уже зарегистрирован!",
            message_id=message.id,
        )
        return

    token = await search_text(message)

    if len(token) < 1:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Укажите токен!",
            message_id=message.id,
        )
        return

    if len(token) > 240:
        token = token.partition("=")[2].partition("&")[0]

    if not await check_token(token):
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Невалидный токен!",
            message_id=message.id,
        )
        return

    from services.user import UserService

    user = await Users.create(user_id=user_id, token=token)

    Config.USER[user_id] = UserService(user_id=user_id, token=token)
    await Config.USER[user_id].run_module()

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.HEART} Пользователь успешно зарегистрирован!",
        message_id=message.id,
    )
