import discord
from discord.ext import commands

import os

from utils.config import load

class Bot(commands.Bot):
    def __init__(self, intents: discord.Intents) -> None:
        super().__init__(Bot.__no_prefix, intents=intents)

    async def on_ready(self) -> None:
        print(f'Logged on as {self.user}!')

    async def setup_hook(self) -> None:
        await super().setup_hook()

        # Load cogs
        for filename in os.listdir("cogs"):
            name, ext = os.path.splitext(filename)
            if ext != ".py":
                continue
            cog_name = "cogs." + name
            await self.load_extension(cog_name)

        # TODO: Move to a special sync command
        # Sync application commands
        # await self.tree.sync()
        # test_guild_id: int | None = load().get("test guild id", None)
        # if test_guild_id is not None:
        #     test_guild = discord.Object(id=test_guild_id)
        #     self.tree.copy_global_to(guild=test_guild)
        #     await self.tree.sync(guild=test_guild)

    def __no_prefix(self, message: discord.Message) -> str:
        # Disables the prefix for regular text commands (slash commands only)
        if message.content.startswith("!"):
            return "#"
        return "!"