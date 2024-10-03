import discord

from bot import Bot
from utils.logger import setup_logger
from utils.config import load as load_config

intents = discord.Intents.default()
intents.message_content = True

setup_logger()

config = load_config()

client = Bot(intents)
client.run(config["token"], log_handler=None) # type: ignore
