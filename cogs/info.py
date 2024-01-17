import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime
from hashlib import sha256
from typing import Any, Optional

from modals.info import SetInfo
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
    async def get(self, interaction: discord.Interaction, user: Optional[discord.User | discord.Member]) -> None:
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
        
        embed=discord.Embed(title=f"{data['firstname']} {data['lastname']}")

        if data.get("email", None) is not None:
            email_digest = sha256(str.encode(data["email"])).hexdigest()
            avatar_url = f"https://gravatar.com/avatar/{email_digest}?s=128&d=404"
            embed.set_thumbnail(url=avatar_url)

        if data.get("github", None) is not None:
            text = f'[{data["github"]}](https://github.com/{data["github"]})'
            embed.add_field(name="GitHub", value=text, inline=True)

        if data.get("linkedin", None) is not None:
            text = f'[{data["linkedin"]}](https://www.linkedin.com/in/{data["linkedin"]})'
            embed.add_field(name="LinkedIn", value=text, inline=True)

        if data.get("birthday", None) is not None:
            L = data["birthday"] # List of date values in the format [(year,) month, day]
            try:
                year = L[0]
                month, day = L[-2:]
                if len(L) == 2:
                    # No year provided, use the next 
                    year = datetime.now().year
                    date = datetime(year=year, month=month, day=day)
                    if date < datetime.now():
                        year += 1
                date = datetime(year=year, month=month, day=day)
            except:
                await interaction.response.send_message(f"Invalid birthday date: {L}")
                return
            timestamp = int(date.timestamp())
            embed.add_field(name="Birthday", value=f'<t:{timestamp}:D>', inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

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
        
        modal = SetInfo(data)
        await interaction.response.send_modal(modal)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Info(bot))