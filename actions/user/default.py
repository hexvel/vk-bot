from pythonping import ping
from vkbottle.user import Message, UserLabeler

from config import Emoji
from models.user import Users
from services.rules.id import FindID
from services.rules.scope import Scope
from utils.helpers import get_random

labeler = UserLabeler()


@labeler.message(Scope(prefix="ф", commands=["пинг", "ping"]))
async def ping_api(message: Message):
    result = ping("api.vk.com", count=4)
    response_times = result.rtt_avg_ms if result.rtt_avg_ms else result.rtt_avg

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.ROCKET} Время ответа: {response_times} мс",
        message_id=message.id,
    )


@labeler.message(
    Scope(prefix="ф", commands=["инфо", "инфа", "info"]),
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

    user_raks = {
        5: "Разработчик",
        4: "Администратор",
        3: "Модератор",
        2: "Агент",
        1: "Пользователь",
    }

    fields_to_display = {
        f"{Emoji.GLASS} Баланс": user.balance,
        f"{Emoji.SPARKLES} Сквад": user.squad,
        f"{Emoji.FIRE} Ранг": user_raks[user.rank],
        f"{Emoji.GIFT} Премиум статус": "Да" if user.premium else "Нет",
        f"{Emoji.SETTINGS} Префикс команд": user.prefix_command,
        f"{Emoji.SETTINGS} Префикс скриптов": user.prefix_script,
        f"{Emoji.SETTINGS} Префикс админа": user.prefix_admin,
        f"{Emoji.SETTINGS} Префикс доверенных": user.trust_prefix,
        f"{Emoji.LIST} Количество игнорируемых": len(user.ignore_list["users"]),
        f"{Emoji.LIST} Количество доверенных": len(user.trust_list["users"]),
    }

    attachment_count = await get_random(start=457239018, _min=1, _max=380)
    attachment = f"photo-224389197_{attachment_count}"

    info_message = "\n".join(
        f"{field}: {value}" for field, value in fields_to_display.items()
    )

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"[id{user.user_id}|{Emoji.USER} Информация о пользователе]:\n{info_message}",
        message_id=message.id,
        attachment=attachment,
    )


@labeler.message(Scope(prefix="ф", commands=["+др", "+fr"]), FindID())
async def add_friend_command_wrapper(message: Message, user_id: int):
    add_friend = await message.ctx_api.friends.add(user_id=user_id)

    if add_friend == 1:
        text = f"{Emoji.OK} [id{user_id}|Пользователю] отправлен запрос на дружбу."
    elif add_friend == 2:
        text = f"{Emoji.OK} Заявка [id{user_id}|пользователя] одобрена."
    elif add_friend == 4:
        text = f"{Emoji.OK} [id{user_id}|Пользователю] отправлен повторный запрос на дружбу."

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=text,
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["лс", "pc"]), FindID())
async def send_message_to_user(message: Message, user_id: int):
    message_split = message.text.split("\n", maxsplit=1)

    if len(message_split) < 2:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Укажите желаемый текст для отправления.",
            message_id=message.id,
        )
        return

    text = message_split[1]
    await message.ctx_api.messages.send(peer_id=user_id, message=text, random_id=0)

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.OK} [id{user_id}|Пользователю] успешно отправлено сообщение.",
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["ид", "id"]), FindID())
async def get_user_id(message: Message, user_id: int):
    if user_id == message.from_id:
        text = f"{Emoji.USER} [id{user_id}| Ваш ID: ] {user_id}"
    else:
        text = (
            f"{Emoji.USER} [id{user_id}| ID пользователя: ] {user_id}\n"
            f"{Emoji.RIGHT} [id{message.from_id}|Ваш ID: ] {message.from_id}"
        )

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=text,
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["-др", "-fr"]), FindID())
async def delete_friend_command_wrapper(message: Message, user_id: int):
    delete_friend = await message.ctx_api.friends.delete(user_id=user_id)

    if delete_friend.success == 1:
        text = f"{Emoji.OK} [id{user_id}|Пользователь] удалён из друзей."
    elif delete_friend.out_request_deleted == 1:
        text = f"{Emoji.OK} Отменяю исходящюю заявку [id{user_id}|пользователю]."
    elif delete_friend.in_request_deleted == 1:
        text = f"{Emoji.OK} Отменяю входящюю заявку от [id{user_id}|пользователя]."

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=text,
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["+чс", "-bl"]), FindID())
async def add_black_list(message: Message, user_id: int):
    add_black_list = await message.ctx_api.account.ban(owner_id=user_id)

    if add_black_list == 1:
        text = f"{Emoji.OK} [id{user_id}|Пользователь] заблокирован."
    else:
        text = f"{Emoji.NO} Не удалось заблокировать [id{user_id}|пользователя]"

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=text,
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["-чс", "-bl"]), FindID())
async def delete_black_list(message: Message, user_id: int):
    delete_black_list = await message.ctx_api.account.unban(owner_id=user_id)

    if delete_black_list == 1:
        text = f"{Emoji.OK} [id{user_id}|Пользователь] разблокирован."
    else:
        text = f"{Emoji.NO} Не удалось разблокировать [id{user_id}|пользователя]"

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=text,
        message_id=message.id,
    )
