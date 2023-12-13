# Adapted from https://discordpy.readthedocs.io/en/latest/intro.html#basic-concepts

import discord

from bot import Bot
from utils.config import load as load_config

intents = discord.Intents.default()
intents.message_content = True

config = load_config()

client = Bot(intents)
client.run(config["token"]) # type: ignore
