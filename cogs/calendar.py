import discord
from discord import app_commands
from discord.ext import commands

import calendar
from datetime import datetime
from typing import Any, Optional

from utils.config import load

class Calendar(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @app_commands.command()
    async def birthdays(self, interaction: discord.Interaction) -> None:
        """Get the different birthdays"""
        try:
            all_data: list[dict[str, Any]] = load("info")
        except FileNotFoundError:
            await interaction.response.send_message(f"Error: No configuration file found.", ephemeral=True)
            return
        
        birthdays: dict[int, dict[int, list[dict[str, Any]]]] = {}
        for data in all_data:
            L = data.get("birthday", None) or []
            if len(L) == 2:
                m, d = L
            elif len(L) == 3:
                _, m, d = L
            else:
                continue # Unkown birthday

            if m not in birthdays:
                birthdays[m] = {}
            if d not in birthdays[m]:
                birthdays[m][d] = []
            birthdays[m][d].append(data)
        
        embed = discord.Embed(title="Birthdays")
        for month in sorted(birthdays):
            embed.add_field(name=calendar.month_name[month], value="\n".join(
                f"{month}/{day}: {data['firstname']} {data['lastname']}"
                for day in sorted(birthdays[month])
                for data in birthdays[month][day]
            ), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Calendar(bot))