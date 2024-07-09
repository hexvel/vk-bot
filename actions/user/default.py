from pythonping import ping
from vkbottle.user import Message, UserLabeler

from config import Emoji
from models.user import Users
from services.rules.id import FindID
from services.rules.scope import Scope

labeler = UserLabeler()


@labeler.message(Scope(prefix=".ф", commands=["пинг", "ping"]))
async def ping_api(message: Message):
    result = ping("api.vk.com", count=4)
    response_times = result.rtt_avg_ms if result.rtt_avg_ms else result.rtt_avg

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.ROCKET} Время ответа: {response_times} мс",
        message_id=message.id,
    )


@labeler.message(
    Scope(prefix=".ф", commands=["инфо", "инфа", "info"]),
    FindID(),
)
async def info(message: Message, user_id: int):
    user = await Users.filter(user_id=user_id).first()

    if not user:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"[id{message.from_id}|{Emoji.WARNING} Пользователь не найден.]",
            message_id=message.id,
        )
        return

    fields_to_display = {
        f"{Emoji.GLASS} Баланс": user.balance,
        f"{Emoji.SPARKLES} Сквад": user.squad,
        f"{Emoji.FIRE} Ранг": user.rank,
        f"{Emoji.GIFT} Премиум статус": "Да" if user.premium else "Нет",
        f"{Emoji.SETTINGS} Префикс команд": user.prefix_command,
        f"{Emoji.SETTINGS} Префикс скриптов": user.prefix_script,
        f"{Emoji.SETTINGS} Префикс админа": user.prefix_admin,
        f"{Emoji.SETTINGS} Префикс доверенных": user.trust_prefix,
        f"{Emoji.LIST} Список игнорируемых": user.ignore_list["users"],
        f"{Emoji.LIST} Список доверенных": user.trust_list["users"],
    }

    info_message = "\n".join(
        f"{field}: {value}" for field, value in fields_to_display.items()
    )

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"[id{user.user_id}|{Emoji.USER} Информация о пользователе]:\n{info_message}",
        message_id=message.id,
    )
