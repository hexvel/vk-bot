import asyncio

from loguru import logger
from vkbottle.api import API
from vkbottle.http import AiohttpClient
from vkbottle.user import User, UserLabeler

from actions.user import user_labelers
from repositories.user import UserManager


class UserService:
    def __init__(self, user_id: int, token: str) -> None:
        self.token = token
        self.user_id = user_id

        self.api = None
        self.task = None
        self.session = None

        # self.commands = user_commands

        self._init_managers()

    def _init_managers(self) -> None:
        # self.alias = AliasManager(self.user_id)
        self.user = UserManager(self.user_id)
        # self.trigger = TriggerManager(self.user_id)

    async def init(self) -> None:
        await self._init_managers_and_api()
        self._init_session()

    async def _init_managers_and_api(self) -> None:
        logger.debug(f"Init managers and api for user {self.user_id}...")
        [await manager.init() for manager in [self.user]]
        logger.success(f"Init managers and api for user {self.user_id}... OK")

        logger.debug(f"Init api for user {self.user_id}...")
        self.api = API(token=self.token, http_client=AiohttpClient())
        logger.success(f"Init api for user {self.user_id}... OK")

    def _init_session(self) -> None:
        logger.debug(f"Init session for user {self.user_id}...")
        user_labeler = UserLabeler()
        for labeler in user_labelers:
            user_labeler.load(labeler)
        self.session = User(api=self.api, labeler=user_labeler)
        setattr(self.session.api, "data", self)
        logger.success(f"Init session for user {self.user_id}... OK")

    async def run_script(self) -> None:
        self.task = asyncio.create_task(
            self.session.run_polling(), name=f"user_{self.user_id}"
        )

    async def stop_session(self) -> None:
        self.task.cancel()

    async def restart_session(self) -> None:
        self.task.cancel()
        await self.run_module()

    async def run_module(self) -> None:
        await self.init()
        logger.debug(f"Run script for user {self.user_id}...")
        await self.run_script()
        logger.success(f"Run script for user {self.user_id}... OK")
