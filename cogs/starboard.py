import discord
from discord.ext import commands

from utils.config import load
from utils.logger import logger


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Starboard(bot))

class Starboard(commands.Cog):
    EMOJIS = ['⭐', '🌟']

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f'Cog {__class__.__name__} ready')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        if payload.emoji.name not in Starboard.EMOJIS:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        
        original_message = await channel.fetch_message(payload.message_id)

        embed = discord.Embed(
            color=discord.Color.blurple(),
            title='1 ⭐',
            description=original_message.content,
            url=original_message.jump_url
        )
        embed.set_author(
            name=original_message.author.name,
            icon_url=original_message.author.avatar.url if original_message.author.avatar else None
        )

        channel_ids: list[int] = load().get('starboard channels', [])
        for channel_id in channel_ids:
            channel = self.bot.get_channel(channel_id)
            if not isinstance(channel, discord.TextChannel):
                continue
            if channel.guild.id != payload.guild_id:
                continue

            # TODO: Send if first reaction, else edit nb of reactions
            await channel.send(embed=embed)
