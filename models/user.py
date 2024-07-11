from tortoise import fields
from tortoise.models import Model


class Users(Model):
    user_id = fields.IntField(pk=True, description="User ID")
    token = fields.TextField(default="None", description="VK token")
    token_vkme = fields.TextField(default="None", description="VKMe token")
    balance = fields.IntField(default=0, description="Balance of the user")
    squad = fields.TextField(default="Hexvel", description="Squad of the user")
    rank = fields.IntField(default=1, description="Rank of the user")
    premium = fields.BooleanField(
        default=False, description="Premium status of the user"
    )
    username = fields.TextField(default="User", description="Username of the user")
    prefix_command = fields.TextField(default=".ф", description="Prefix for commands")
    prefix_script = fields.TextField(default=".у", description="Prefix for scripts")
    prefix_admin = fields.TextField(
        default=".й", description="Prefix for admin commands"
    )
    trust_prefix = fields.TextField(default="#", description="Prefix for trusted users")
    ignore_list = fields.JSONField(
        default={"users": []}, description="List of users to ignore"
    )
    trust_list = fields.JSONField(
        default={"users": []}, description="List of trusted users"
    )
    alias = fields.JSONField(default={"items": []}, description="List of aliases")
