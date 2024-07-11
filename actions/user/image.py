from loguru import logger
from vkbottle import PhotoMessageUploader
from vkbottle.user import Message, UserLabeler

from config import Emoji
from mylib.qr import QRCode
from services.rules.scope import Scope
from utils.helpers import get_attachment_doc

labeler = UserLabeler()


@labeler.message(Scope(prefix=".ф", commands=["qrcode"]))
async def qrcode(message: Message):
    try:
        if len(message.text.split()) <= 2:
            await message.ctx_api.messages.edit(
                peer_id=message.peer_id,
                message=f"{Emoji.WARNING} Укажите вложение для генерации QR-кода.",
                message_id=message.id,
            )
            return

        link = message.text.split(maxsplit=2)[2]
        attachment = await get_attachment_doc(message)

        if not attachment:
            qr = QRCode(link, with_background=False)
        else:
            if not message.attachments or not message.attachments[0].doc:
                await message.ctx_api.messages.edit(
                    peer_id=message.peer_id,
                    message=f"{Emoji.WARNING} Укажите тип [изображение] для генерации QR-кода.",
                    message_id=message.id,
                )
                return

            qr = QRCode(link, attachment)

        qr.generate_qr_code()
        qr.resize_background_image()
        qr.blend_images()
        _bytes = qr.save_image()

        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.LOADING} Ожидайте генерацию QR-кода.",
            message_id=message.id,
        )

        uploader = PhotoMessageUploader(message.ctx_api)
        photo = await uploader.upload(file_source=_bytes, peer_id=message.peer_id)

        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.OK} QR-код генерирован.",
            message_id=message.id,
            attachment=photo,
        )

    except Exception as e:
        logger.exception(e)
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message=f"{Emoji.WARNING} Произошла ошибка при генерации QR-кода.",
            message_id=message.id,
        )
