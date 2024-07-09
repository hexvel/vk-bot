from models.user import Aliases


class AliasManager:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.aliases = {}

    async def init(self):
        data = await Aliases.filter(user_id=self.user_id).all()
        for alias in data:
            self.aliases[alias.name] = {
                "name": alias.name,
                "command": alias.command,
            }

    def get_alias(self, alias):
        return self.aliases[alias]["command"]

    def exists(self, alias):
        return alias in self.aliases

    async def set_alias(self, alias: dict):
        self.aliases[alias["name"]] = alias
        await Aliases.create(
            user_id=self.user_id, name=alias["name"], command=alias["command"]
        )

    async def del_alias(self, name: str):
        del self.aliases[name]
        await Aliases.filter(user_id=self.user_id, name=name).delete()
