# Adapted from https://discordpy.readthedocs.io/en/latest/intro.html#basic-concepts

import discord

from utils.config import load as load_config

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

config = load_config()

client = MyClient(intents=intents)
client.run(config["token"]) # type: ignore
