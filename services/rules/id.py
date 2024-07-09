import re

from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message


class FindID(ABCRule[Message]):
    async def check(self, event: Message):
        message = event.text
        data = dict()

        if event.reply_message:
            data["user_id"] = event.reply_message.from_id

        elif len(message.split(maxsplit=2)) < 3:
            data["user_id"] = event.from_id

        else:
            user_id_match = re.search(r"\[id(\d+)\|\S+]", message)
            if user_id_match:
                data["user_id"] = int(user_id_match.group(1))
            else:
                user_id_match = re.search(r"\b\d{7,15}\b", message)
                if user_id_match:
                    data["user_id"] = int(user_id_match.group())
                else:
                    data["user_id"] = event.from_id

        return data
