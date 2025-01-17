import random
from contextlib import suppress

from vkbottle import API, AiohttpClient, VKAPIError
from vkbottle.user import Message


async def get_attachment(message: Message, attachment_type: str):
    attachment = None
    if message.attachments:
        attachment_item = getattr(message.attachments[0], attachment_type, None)
    elif message.reply_message and message.reply_message.attachments:
        attachment_item = getattr(
            message.reply_message.attachments[0], attachment_type, None
        )
    else:
        attachment_item = None

    if attachment_item:
        attachment = (
            attachment_item.url
            if attachment_type == "doc"
            else attachment_item.sizes[-1].url
        )

    return attachment


async def get_attachment_photo(message: Message):
    return await get_attachment(message, "photo")


async def get_attachment_doc(message: Message):
    return await get_attachment(message, "doc")


def get_random(start: int = 0, _min: int = 1, _max: int = 100):
    attachment_count = start
    image_candidate = random.randint(_min, _max)
    attachment_count += image_candidate

    return attachment_count


async def search_text(message: Message) -> str:
    if message.reply_message:
        return message.reply_message.text
    else:
        return message.text


async def check_token(token: str, app_id: int = 6121396) -> bool:
    ok = False
    api = API(token=token, http_client=AiohttpClient())
    with suppress(VKAPIError, TypeError):
        apps = await api.apps.get()
        ok = True if apps.items[0].id in [app_id] else False
    await api.http_client.close()
    return ok
