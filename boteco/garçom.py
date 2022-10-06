import discord
from discord.ext import commands, tasks
from loguru import logger
from slugify import slugify

from boteco.tracker import VoiceChannelTracker


class Garçom(commands.Cog):
    def __init__(self, voice_channel_tracker: VoiceChannelTracker):
        self.voice_channel_tracker = voice_channel_tracker
        self.close_empty_tables.start()

    @tasks.loop(minutes=1)
    async def close_empty_tables(self):
        if len(self.voice_channel_tracker) == 0:
            return

        logger.info("Running job: close_empty_tables")
        await self.voice_channel_tracker.delete_empty_channels()

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ):
        channel = before.channel or after.channel
        if not channel:
            logger.warning(
                f"Couldn't get channel on state update. member={member}, before={before.channel}, after={after.channel}"
            )
            return

        if not channel.category or channel.category.name != "boteco":
            return

        if len(channel.members) == 0:
            logger.info(f"Channel to be removed. channel={channel.name!r}")
            self.voice_channel_tracker.track(channel)

        if len(channel.members) > 0:
            self.voice_channel_tracker.stop_tracking(channel)

    @commands.command()
    async def ping(self, ctx: commands.Context, *args):
        await ctx.message.reply("pong")

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def boteco(self, ctx, command: str, *args):
        if command not in ["build", "abrir"]:
            return

        if not (boteco := discord.utils.get(ctx.guild.categories, name="boteco")):
            boteco = await ctx.guild.create_category("boteco")

        if not (new_table := discord.utils.get(boteco.channels, name="peca-uma-mesa")):
            new_table = await boteco.create_text_channel("peca-uma-mesa")

        await ctx.message.add_reaction("✅")
        await ctx.channel.send(
            "Boteco criado! Você pode pedir uma mesa a partir de qualquer canal ou "
            f"direto do {new_table.mention}. Por exemplo: `!mesa botecobot`."
        )

    @commands.command()
    async def mesa(self, ctx, *args):
        boteco = discord.utils.get(ctx.guild.categories, name="boteco")
        tables = [table.name for table in boteco.voice_channels]

        if not args:
            logger.warning("missing table name!")
            await ctx.channel.send(
                "Opa, faltou dar um nome para a sua mesa, tente algo como `!mesa vim melhor que emacs` hahaha 😅"
            )
            return

        new_table = slugify("mesa " + " ".join(args))
        if new_table in tables:
            logger.warning(
                "This table already exists. new_table={new_table!r}, tables={tables!r}"
            )
            await ctx.channel.send(
                "Opa, uma mesa já existe com esse nome, mas sinta-se à vontade e participe da conversa! 😄 🍺"
            )
            return

        channel = await boteco.create_voice_channel(new_table, user_limit=25)
        self.voice_channel_tracker.track(channel)
        await ctx.message.add_reaction("🍻")
        await ctx.channel.send(f"Mesa disponível no **#boteco**")
