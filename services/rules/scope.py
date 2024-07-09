from typing import List, Optional, Union

from vkbottle.dispatch.rules import ABCRule
from vkbottle.user import Message


class Scope(ABCRule[Message]):
    def __init__(
        self,
        prefix: Optional[str],
        commands: Union[str, List[str]],
        rank: Optional[int] = 1,
    ):
        self.prefix = prefix
        self.commands = commands
        self.rank = rank

    async def check(self, message: Message):
        data = message.ctx_api.data

        if data.user.rank < self.rank:
            return False
        if not bool(message.out):
            return False
        if not message.text:
            return False

        # if message.text.split()[0].lower() in list(data.alias.aliases.keys()):
        #     alias_command = data.alias.get_alias(message.text.split()[0].lower())
        #     message.text = message.text.replace(message.text.split()[0], alias_command)

        command = message.text.split("\n")[0].split()
        if len(command) < 2:
            return False

        if self.prefix == "ф":
            self.prefix = ["ф", data.user.get_prefix_commands()]
        if self.prefix == ".у":
            self.prefix = [".у", data.user.get_prefix_scripts()]
        if self.prefix == ".й":
            self.prefix = [".й", data.user.get_prefix_admin()]

        return bool(
            command[0].lower() in self.prefix and command[1].lower() in self.commands
        )
