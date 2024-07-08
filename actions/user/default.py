from pythonping import ping
from vkbottle.user import Message, UserLabeler

from config import Emoji
from services.rules.scope import Scope

labeler = UserLabeler()


@labeler.message(Scope(prefix=".ф", commands=["пинг", "ping"]))
async def test(message: Message):
    result = ping("api.vk.com", count=4)
    response_times = result.rtt_avg_ms if result.rtt_avg_ms else result.rtt_avg

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.ROCKET} Время ответа: {response_times} мс",
        message_id=message.id,
    )


@labeler.message(Scope(prefix=".ф", commands=["инфо", "инфа", "info"]))
async def info(message: Message):
    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"Информация о пользователе: {message.user_id}",
        message_id=message.id,
    )
