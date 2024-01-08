import discord

from typing import Any

class SetInfo(discord.ui.Modal, title="Information settings"):
    name = discord.ui.TextInput(
        label="Full name",
        style=discord.TextStyle.short,
        placeholder="Hello WORLD",
        required=True
    )
    email = discord.ui.TextInput(
        label="Email",
        style=discord.TextStyle.short,
        placeholder="hello.world@discord.com",
        required=True
    )
    github = discord.ui.TextInput(
        label="GitHub handle",
        style=discord.TextStyle.short,
        required=False
    )
    linkedin = discord.ui.TextInput(
        label="LinkedIn handle",
        style=discord.TextStyle.short,
        required=False
    )
    birthday = discord.ui.TextInput(
        label="Birthday",
        style=discord.TextStyle.short,
        placeholder="1999/12/31 or 12/31",
        required=False
    )

    def __init__(self, data: dict[str, Any], callback) -> None:
        firstname = data.get("firstname", None) or ""
        lastname = data.get("lastname", None) or ""
        self.name.default = f"{firstname} {lastname}" if firstname and lastname else firstname or lastname or ""
        self.email.default = data.get("email", None) or ""
        self.github.default = data.get("github", None) or ""
        self.linkedin.default = data.get("linkedin", None) or ""
        self.birthday.default = "/".join(data.get("birthday", None) or [])
        super().__init__()
        self.callback = callback

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # TODO: Data validation
        await self.callback(interaction, self)

    async def on_error(self, interaction: discord.Interaction, exception: Exception) -> None:
        await interaction.response.send_message(f"Error: {exception}", ephemeral=True)