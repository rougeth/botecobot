from discord import Intents

from boteco import config
from boteco.bot import Bot

intents = Intents.default()
intents.message_content = True

bot = Bot(command_prefix="!", intents=intents)

if __name__ == "__main__":
    bot.run(config.DISCORD_TOKEN)
