from loguru import logger
from vkbottle.user import Message


async def get_attachment_photo(message: Message):
    if message.attachments:
        if message.attachments[0].photo:
            attachment = message.attachments[0].photo.sizes[-1].url
        else:
            attachment = None

    elif message.reply_message.attachments:
        if message.reply_message.attachments[0].photo:
            attachment = message.reply_message.attachments[0].photo.sizes[-1].url
        else:
            attachment = None
    else:
        attachment = None

    return attachment


async def get_attachment_doc(message: Message):
    if message.attachments:
        if message.attachments[0].doc:
            attachment = message.attachments[0].doc.url
        else:
            attachment = None

    elif message.reply_message.attachments:
        if message.reply_message.attachments[0].doc:
            attachment = message.reply_message.attachments[0].doc.url
        else:
            attachment = None
    else:
        attachment = None

    return attachment
