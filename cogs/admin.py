import discord
from discord import app_commands
from discord.ext import commands

from utils.config import load

class Admin(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def sync(self, interaction: discord.Interaction) -> None:
        """Synchronize the commands"""
        admin_ids = load().get("admins id", [])
        if admin_ids and interaction.user.id not in admin_ids:
            await interaction.response.send_message("You do not have enough permissions do use this command.", ephemeral=True)
            return

        await self.bot.tree.sync()
        test_guild_ids = load().get("test guild ids", [])
        for test_guild_id in test_guild_ids:
            test_guild = discord.Object(id=test_guild_id)
            self.bot.tree.copy_global_to(guild=test_guild)
            await self.bot.tree.sync(guild=test_guild)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Admin(bot))