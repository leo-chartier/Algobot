import discord
from discord.ext import commands

from utils.config import load
from utils.logger import logger


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Starboard(bot))

class Starboard(commands.Cog):
    EMOJIS = ['⭐', '🌟']
    CUSTOM_EMOJIS: list[int]

    # TODO: Move to DB for permanent storage
    history: dict[int, dict[int, int]] = {}
    """{original_message_id: {channel_id: new_message_id}}"""

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        Starboard.CUSTOM_EMOJIS = load("bot").get("starboard custom emojis", [])

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        logger.info(f'Cog {__class__.__name__} ready')
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent) -> None:
        await self._on_raw_reaction_change(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent) -> None:
        await self._on_raw_reaction_change(payload)

    async def _on_raw_reaction_change(self, payload: discord.RawReactionActionEvent) -> None:
        if not self._is_valid_emoji(payload.emoji):
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None or not isinstance(channel, discord.TextChannel):
            return
        
        original_message = await channel.fetch_message(payload.message_id)

        embed = self._generate_embed(original_message)

        channel_ids: list[int] = load().get('starboard channels', [])
        for channel_id in channel_ids:
            if channel.guild.id == payload.guild_id:
                if embed is None:
                    await self._delete(channel_id, original_message.id)
                else:
                    await self._send_embed(embed, channel_id, original_message.id)

    def _is_valid_emoji(self, emoji: discord.PartialEmoji | discord.Emoji | str):
        if isinstance(emoji, str):
            return emoji in self.EMOJIS
        
        if isinstance(emoji, discord.PartialEmoji):
            if emoji.is_unicode_emoji:
                return emoji.name in self.EMOJIS
            if emoji.is_custom_emoji:
                return emoji.id in self.CUSTOM_EMOJIS
        
        if isinstance(emoji, discord.Emoji):
            return emoji.id in self.CUSTOM_EMOJIS
        
        return False

    def _generate_embed(self, original_message: discord.Message) -> discord.Embed | None:
        nb_reactions = 0
        for reaction in original_message.reactions:
            if self._is_valid_emoji(reaction.emoji):
                nb_reactions += reaction.count
        
        if nb_reactions == 0:
            return None

        embed = discord.Embed(
            color=discord.Color.blurple(),
            title=f'{nb_reactions} ⭐',
            description=original_message.content,
            url=original_message.jump_url
        )
        embed.set_author(
            name=original_message.author.display_name,
            icon_url=original_message.author.avatar.url if original_message.author.avatar else None
        )
        
        return embed
    
    async def _send_embed(self, embed: discord.Embed, channel_id: int, original_message_id: int) -> None:
        channel = self.bot.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        if original_message_id not in self.history:
            self.history[original_message_id] = {}
        message_history = self.history[original_message_id]
        
        if channel_id in message_history:
            # Edit the existing one
            message_id = message_history[channel_id]
            message = await channel.fetch_message(message_id)
            await message.edit(embed=embed)
        
        else:
            # Send a new message
            new_message = await channel.send(embed=embed)
            message_history[channel_id] = new_message.id
    
    async def _delete(self, channel_id: int, original_message_id: int) -> None:
        channel = self.bot.get_channel(channel_id)
        if not isinstance(channel, discord.TextChannel):
            return

        if original_message_id not in self.history:
            return
        message_history = self.history[original_message_id]
        
        if channel_id not in message_history:
            return
        
        message_id = message_history[channel_id]
        message = await channel.fetch_message(message_id)
        
        await message.delete()
        message_history.pop(channel_id)
