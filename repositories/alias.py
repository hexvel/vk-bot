from models.user import Users


class AliasManager:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.aliases = {}

    async def init(self):
        data = await Users.filter(user_id=self.user_id).first()
        for alias in data.alias["items"]:
            self.aliases[alias["name"]] = {
                "name": alias["name"],
                "command": alias["command"],
            }

    def get_alias(self, alias):
        return self.aliases[alias]["command"]

    def exists(self, alias):
        return alias in self.aliases

    async def set_alias(self, alias: dict):
        self.aliases[alias["name"]] = alias
        data = await Users.filter(user_id=self.user_id).first()

        data.alias["items"].append(alias)
        await data.save(update_fields=["alias"])

    async def delete_alias(self, name: str):
        del self.aliases[name]

        data = await Users.filter(user_id=self.user_id).first()
        data.alias["items"] = [
            alias for alias in data.alias["items"] if alias["name"] != name
        ]
        await data.save(update_fields=["alias"])
