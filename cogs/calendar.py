import discord
from discord import app_commands
from discord.ext import commands

import calendar
from datetime import date
from typing import Any

from utils.config import load
from utils.logger import logger

EMBED_LIMIT = 6000

class Calendar(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f"Cog {__class__.__name__} ready")

    @app_commands.command()
    async def birthdays(self, interaction: discord.Interaction) -> None:
        """Get the different birthdays"""
        try:
            all_data: list[dict[str, Any]] = load("info")
        except FileNotFoundError:
            await interaction.response.send_message(f"Error: No configuration file found.", ephemeral=True)
            return
        
        today = date.today()
        birthdays: dict[int, list[tuple[date, str]]] = {}
        for data in all_data:
            L = data.get("birthday", None) or []
            if len(L) == 2:
                m, d = L
            elif len(L) == 3:
                _, m, d = L
            else:
                continue # Unkown birthday

            bdate = date(today.year, m, d)
            if bdate < today:
                bdate = date(today.year + 1, m, d)
                m += 12

            fullname = f"{data['firstname']} {data['lastname']}"
            
            if m not in birthdays:
                birthdays[m] = []
            birthdays[m].append((bdate, fullname))

        embed = discord.Embed(title="Birthdays")
        for m in sorted(birthdays):
            copy = embed.copy()

            L = birthdays[m]
            lines = "\n".join(
                f"{d.day}: {fullname}"
                for d, fullname in sorted(L, key=lambda x: x[0])
            )

            name = calendar.month_name[m % 12]
            if m > 12:
                name += f" {L[0][0].year}"

            copy.add_field(name=name, value=lines, inline=False)
            if len(copy) > EMBED_LIMIT:
                break
            embed = copy
        
        await interaction.response.send_message(embed=embed, ephemeral=True)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Calendar(bot))