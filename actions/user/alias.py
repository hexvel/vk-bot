from vkbottle.user import Message, UserLabeler

from config import Emoji
from services.rules.scope import Scope

labeler = UserLabeler()


@labeler.message(Scope(prefix="ф", commands=["+алиас"]))
async def add_alias(message: Message):
    data = message.ctx_api.data.alias

    if (
        len(message.text.split("\n")[0].split()) <= 2
        or len(message.text.split("\n")) < 2
    ):
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Укажите правильные аргументы.",
            message_id=message.id,
        )
        return

    alias = message.text.split("\n", maxsplit=2)[0].split()[2].strip()
    command = message.text.split("\n")[1].strip()

    if data.exists(alias):
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Алиас уже существует",
            message_id=message.id,
        )
        return

    new_alias = dict(name=alias, command=command)
    await data.set_alias(new_alias)

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.OK} Алиас добавлен",
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["-алиас"]))
async def delete_alias(message: Message):
    data = message.ctx_api.data.alias

    if len(message.text.split()) <= 2:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Укажите правильные аргументы.",
            message_id=message.id,
        )
        return

    alias = message.text.split()[2].strip()

    if not data.exists(alias):
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Алиас не существует",
            message_id=message.id,
        )

    await data.delete_alias(alias)

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id,
        message=f"{Emoji.OK} Алиас удален",
        message_id=message.id,
    )


@labeler.message(Scope(prefix="ф", commands=["алиасы"]))
async def get_alias(message: Message):
    data = message.ctx_api.data.alias

    aliases = list(data.aliases.keys())
    if not aliases:
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.LIST} Список алиасов пуст",
            message_id=message.id,
        )
        return

    text = f"{Emoji.SETTINGS} Список алиасов:"

    for alias in aliases:
        alias_data = data.aliases[alias]
        text += f"\n--> {alias_data['name']} | {alias_data['command']}"

    await message.ctx_api.messages.edit(
        peer_id=message.peer_id, message=text, message_id=message.id
    )
