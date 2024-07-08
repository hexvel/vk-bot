from models.user import Users


class UserManager:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.user = None
        self.token = None
        self.token_vkme = None
        self.balance = None
        self.squad = None
        self.rank = None
        self.premium = None
        self.username = None
        self.trust_list = None
        self.prefix_command = None
        self.prefix_script = None
        self.prefix_admin = None
        self.trust_prefix = None
        self.ignore_list = None

    async def init(self):
        self.user = await Users.filter(user_id=self.user_id).first()
        self.token = self.user.token
        self.token_vkme = self.user.token_vkme
        self.balance = self.user.balance
        self.squad = self.user.squad
        self.rank = self.user.rank
        self.premium = self.user.premium
        self.username = self.user.username
        self.trust_list = self.user.trust_list["users"]
        self.prefix_command = self.user.prefix_command
        self.prefix_script = self.user.prefix_script
        self.prefix_admin = self.user.prefix_admin
        self.trust_prefix = self.user.trust_prefix
        self.ignore_list = self.user.ignore_list["users"]

    def get_nick(self) -> str:
        return self.nick

    async def set_nick(self, nick: str):
        self.username = nick
        await Users.filter(user_id=self.user_id).update(username=self.username)

    def get_rank(self) -> int:
        return self.rank

    async def set_rank(self, rank: int):
        self.rank = rank
        await Users.filter(user_id=self.user_id).update(rank=self.rank)

    def get_balance(self) -> str:
        return self.balance

    async def set_balance(self, balance: int, action: str):
        balance = self.balance + balance if action == "+" else self.balance - balance
        self.balance = balance
        await Users.filter(user_id=self.user_id).update(balance=self.balance)

    def get_ignore_list(self) -> list:
        return self.ignore_list

    async def set_ignore_list(self, user_id: int, action: str):
        self.ignore_list.append(user_id) if action == "+" else self.ignore_list.remove(
            user_id
        )
        await Users.filter(user_id=self.user_id).update(
            ignore_list=dict(users=self.ignore_list)
        )

    def get_trusted_list(self) -> list:
        return self.trust_list

    async def set_trusted_list(self, user_id: int, action: str):
        self.trust_list.append(user_id) if action == "+" else self.trust_list.remove(
            user_id
        )
        await Users.filter(user_id=self.user_id).update(
            trust_list=dict(users=self.trust_list)
        )

    def get_prefix_commands(self) -> str:
        return self.prefix_command

    async def set_prefix_commands(self, prefix: str):
        self.prefix_command = prefix
        await Users.filter(user_id=self.user_id).update(
            prefix_command=self.prefix_command
        )

    def get_prefix_scripts(self) -> str:
        return self.prefix_script

    async def set_prefix_scripts(self, prefix: str):
        self.prefix_script = prefix
        await Users.filter(user_id=self.user_id).update(
            prefix_script=self.prefix_script
        )

    def get_prefix_trust(self) -> str:
        return self.trust

    async def set_prefix_admin(self, prefix: str):
        self.prefix_admin = prefix
        await Users.filter(user_id=self.user_id).update(prefix_admin=self.prefix_admin)

    def get_prefix_admin(self) -> str:
        return self.prefix_admin
