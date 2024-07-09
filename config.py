import os

from dotenv import load_dotenv

load_dotenv()

tortoise_orm = {
    "connections": {
        "default": f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:3306/{os.getenv('DB_NAME')}"
    },
    "apps": {
        "models": {
            "models": ["models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}


class Config:
    USER = {}


class Emoji:
    SMILE = "😄"
    SAD = "☹️"
    HEART = "❤️"
    SUN = "☀️"
    SETTINGS = "⚙️"
    CLOUD = "☁️"
    THUMBS_UP = "👍"
    THUMBS_DOWN = "👎"
    BELL = "🔔"
    MUSIC = "🎵"
    BUG = "🐞"
    FLAG = "🏁"
    GIFT = "🎁"
    FIRE = "🔥"
    PARTY = "🎉"
    PART_ALTERNATING = "🕳️"
    PENCIL = "✏️"
    PENCIL2 = "✒️"
    ROCKET = "🚀"
    SCISSORS = "✂️"
    WATER = "💧"
    WARNING = "⚠️"
    GLASS = "🍹"
    BEER = "🍺"
    COFFEE = "☕️"
    OK = "✅"
    CROSS = "❌"
    CLOCK = "⏰"
    CLOCK10 = "🕙"
    CLOCK11 = "🕚"
    CLOCK2 = "🕑"
    CLOCK3 = "🕒"
    CLOCK4 = "🕓"
    CLOCK5 = "🕔"
    CLOCK6 = "🕕"
    CLOCK7 = "🕖"
    CLOCK8 = "🕗"
    CLOCK9 = "🕘"
    STOPWATCH = "⏱️"
    ALARM_CLOCK = "⏰"
    HOURGLASS = "⌛️"
    HOURGLASS2 = "⏳"
    SPARKLES = "✨"
    ANGLE = "💭"
    ANGLE2 = "💡"
    EXCLAMATION = "❗"
    QUESTION = "❓"
    BANG = "💥"
    BOOM = "💥"
    FIRE = "🔥"
    SKULL = "💀"
    SKULL2 = "☠️"
    SKULL3 = "💀"
    LIST = "📃"
    USER = "👤"
