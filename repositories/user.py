from models.user import Users


class UserManager:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None

    async def init(self):
        self.user = await Users.filter(user_id=self.user_id).first()

    @property
    def user_exists(self):
        return self.user is not None

    @property
    def token(self):
        return self.user.token if self.user else "None"

    @property
    def token_vkme(self):
        return self.user.token_vkme if self.user else "None"

    @property
    def balance(self):
        return self.user.balance if self.user else 0

    @property
    def squad(self):
        return self.user.squad if self.user else "Hexvel"

    @property
    def rank(self):
        return self.user.rank if self.user else 1

    @property
    def premium(self):
        return self.user.premium if self.user else False

    @property
    def username(self):
        return self.user.username if self.user else "User"

    @property
    def prefix_command(self):
        return self.user.prefix_command if self.user else ".ф"

    @property
    def prefix_script(self):
        return self.user.prefix_script if self.user else ".у"

    @property
    def prefix_admin(self):
        return self.user.prefix_admin if self.user else ".й"

    @property
    def trust_prefix(self):
        return self.user.trust_prefix if self.user else "#"

    @property
    def ignore_list(self):
        return self.user.ignore_list["users"] if self.user else []

    @property
    def trust_list(self):
        return self.user.trust_list["users"] if self.user else []

    async def set_username(self, username: str):
        await self.user.update(username=username)

    async def set_rank(self, rank: int):
        await self.user.update(rank=rank)

    async def set_balance(self, amount: int, action: str):
        current_balance = self.user.balance
        new_balance = (
            current_balance + amount if action == "+" else current_balance - amount
        )
        await self.user.update(balance=new_balance)

    async def add_to_ignore_list(self, user_id: int):
        ignore_list = self.user.ignore_list.get("users", [])
        ignore_list.append(user_id)
        await self.user.update(ignore_list={"users": ignore_list})

    async def remove_from_ignore_list(self, user_id: int):
        ignore_list = self.user.ignore_list.get("users", [])
        if user_id in ignore_list:
            ignore_list.remove(user_id)
            await self.user.update(ignore_list={"users": ignore_list})

    async def add_to_trust_list(self, user_id: int):
        trust_list = self.user.trust_list.get("users", [])
        trust_list.append(user_id)
        await self.user.update(trust_list={"users": trust_list})

    async def remove_from_trust_list(self, user_id: int):
        trust_list = self.user.trust_list.get("users", [])
        if user_id in trust_list:
            trust_list.remove(user_id)
            await self.user.update(trust_list={"users": trust_list})
