import discord
from discord.ext import commands

import os

from utils.config import load
from utils.logger import logger

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents) -> None:
        self.nickname: str = load().get("nickname", "")
        super().__init__(Bot.__no_prefix, intents=intents)

    async def on_ready(self) -> None:
        if self.nickname:
            for guild in self.guilds:
                await guild.me.edit(nick=self.nickname)

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.CustomActivity("Rejoignez ALGOSUP!")
        )

        logger.info(f'Logged on as {self.user}!')

    async def on_member_update(self, before: discord.Member, after: discord.Member) -> None:
        if after != after.guild.me or not self.nickname:
            return
        if after.nick and after.nick != self.nickname:
            await after.guild.me.edit(nick=self.nickname)

    async def setup_hook(self) -> None:
        await super().setup_hook()

        # Load cogs
        for filename in os.listdir("cogs"):
            name, ext = os.path.splitext(filename)
            if ext != ".py":
                continue
            cog_name = "cogs." + name
            await self.load_extension(cog_name)

    def __no_prefix(self, message: discord.Message) -> str:
        # Disables the prefix for regular text commands (slash commands only)
        if message.content.startswith("!"):
            return "#"
        return "!"