from discord.ext import commands


class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.load_extension("setup")
