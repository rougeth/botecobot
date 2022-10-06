from discord.ext.commands import Bot
from loguru import logger

from boteco.garçom import Garçom
from boteco.tracker import VoiceChannelTracker


async def setup(bot: Bot):
    voice_channel_tracker = VoiceChannelTracker()
    await bot.add_cog(Garçom(voice_channel_tracker))
