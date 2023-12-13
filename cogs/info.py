import discord
from discord import app_commands
from discord.ext import commands

from typing import Any, Optional

from utils.config import load

# TODO: Use a real database

class Info(commands.Cog):

    FIELDS = {
        "firstname": str,
        "lastname": str,
        "email": str,
        "github": str | None,
        "linkedin": str | None,
        "birthday": list[int] | None
        # The "discord" field is not included as it should be constant
    }

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    group = app_commands.Group(name="info", description="Get or set generic information about you or someone else")

    @group.command()
    async def get(self, interaction: discord.Interaction, user: Optional[discord.User]) -> None:
        """Get information about you or someone else"""
        if user is None:
            user = interaction.user
        
        try:
            all_data: list[dict[str, Any]] = load("info")
        except FileNotFoundError:
            await interaction.response.send_message(f"Error: No configuration file found.", ephemeral=True)
            return

        for data in all_data:
            if data.get("discord", None) == user.id:
                break
        else:
            await interaction.response.send_message(f"Error: No data found about {user.mention}", ephemeral=True)
            return
        
        # TODO: Show modal

    @group.command()
    async def set(self, interaction: discord.Interaction) -> None:
        """Set your information"""
        try:
            all_data: list[dict[str, Any]] = load("info")
        except FileNotFoundError:
            await interaction.response.send_message(f"Error: No configuration file found.", ephemeral=True)
            return

        for data in all_data:
            if data.get("discord", None) == interaction.user.id:
                break
        else:
            data = {"discord": interaction.user.id}
        
        # TODO: Show modal and save

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot))