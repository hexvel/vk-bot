import asyncio

from loguru import logger
from vkbottle.api import API
from vkbottle.http import AiohttpClient
from vkbottle.bot import Bot, BotLabeler


class BotService:
    def __init__(self, group_id: int, token: str) -> None:
        self.token = token
        self.group_id = group_id

        self.api = None
        self.task = None
        self.session = None

        # self.commands = user_commands

        self._init_managers()

    def _init_managers(self) -> None: ...
        # self.bot = BotManager(self.group_id)

    async def init(self) -> None:
        await self._init_managers_and_api()
        self._init_session()

    async def _init_managers_and_api(self) -> None:
        # logger.debug(f"Init managers and api for group {self.group_id}...")
        # [await manager.init() for manager in [self.bot, self.alias]]
        # logger.success(f"Init managers and api for user {self.group_id}... OK")

        logger.debug(f"Init api for group {self.group_id}...")
        self.api = API(token=self.token, http_client=AiohttpClient())
        logger.success(f"Init api for group {self.group_id}... OK")

    def _init_session(self) -> None:
        logger.debug(f"Init session for group {self.group_id}...")
        bot_labeler = BotLabeler()
        for labeler in []:
            bot_labeler.load(labeler)
        self.session = Bot(api=self.api, labeler=bot_labeler)
        setattr(self.session.api, "data", self)
        logger.success(f"Init session for group {self.group_id}... OK")

    async def run_script(self) -> None:
        self.task = asyncio.create_task(
            self.session.run_polling(), name=f"group_{self.group_id}"
        )

    async def stop_session(self) -> None:
        self.task.cancel()

    async def restart_session(self) -> None:
        self.task.cancel()
        await self.run_module()

    async def run_module(self) -> None:
        await self.init()
        logger.debug(f"Run script for group {self.group_id}...")
        await self.run_script()
        logger.success(f"Run script for group {self.group_id}... OK")
