from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `users` (
    `user_id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT 'User ID',
    `token` LONGTEXT NOT NULL  COMMENT 'VK token',
    `token_vkme` LONGTEXT NOT NULL  COMMENT 'VKMe token',
    `balance` INT NOT NULL  COMMENT 'Balance of the user' DEFAULT 0,
    `squad` LONGTEXT NOT NULL  COMMENT 'Squad of the user',
    `rank` INT NOT NULL  COMMENT 'Rank of the user' DEFAULT 1,
    `premium` BOOL NOT NULL  COMMENT 'Premium status of the user' DEFAULT 0,
    `username` LONGTEXT NOT NULL  COMMENT 'Username of the user',
    `prefix_command` LONGTEXT NOT NULL  COMMENT 'Prefix for commands',
    `prefix_script` LONGTEXT NOT NULL  COMMENT 'Prefix for scripts',
    `prefix_admin` LONGTEXT NOT NULL  COMMENT 'Prefix for admin commands',
    `trust_prefix` LONGTEXT NOT NULL  COMMENT 'Prefix for trusted users',
    `ignore_list` JSON NOT NULL  COMMENT 'List of users to ignore',
    `trust_list` JSON NOT NULL  COMMENT 'List of trusted users',
    `alias` JSON NOT NULL  COMMENT 'List of aliases'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
