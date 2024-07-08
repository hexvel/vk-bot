from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger
from tortoise import Tortoise

from config import Config, tortoise_orm
from models.user import Users
from services.user import UserService

logger.disable("vkbottle")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Tortoise.init(tortoise_orm)
    await Tortoise.generate_schemas()

    for user in await Users.all():
        if not user.token:
            await Users.filter(id=user.user_id).update(token="")
        else:
            Config.USER[user.user_id] = UserService(
                user_id=user.user_id, token=user.token
            )

            await Config.USER[user.user_id].run_module()
    yield
    await Tortoise.close_connections()
    logger.debug("App stopped")


app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=4200, log_level="warning")
