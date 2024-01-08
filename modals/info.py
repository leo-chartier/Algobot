import discord

from typing import Any

from utils.config import load, save

class SetInfo(discord.ui.Modal, title="Information settings"):
    name = discord.ui.TextInput(
        label="Full name",
        style=discord.TextStyle.short,
        placeholder="First Name LAST NAME",
        required=True
    )
    email = discord.ui.TextInput(
        label="Email",
        style=discord.TextStyle.short,
        placeholder="firstname.lastname@discord.com",
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

    def __init__(self, data: dict[str, Any]) -> None:
        firstname = data.get("firstname", None) or ""
        lastname = data.get("lastname", None) or ""
        self.name.default = f"{firstname} {lastname}" if firstname and lastname else firstname or lastname or ""
        self.email.default = data.get("email", None) or ""
        self.github.default = data.get("github", None) or ""
        self.linkedin.default = data.get("linkedin", None) or ""
        self.birthday.default = "/".join(str(x) for x in data.get("birthday", None) or [])
        super().__init__()

    async def on_submit(self, interaction: discord.Interaction) -> None:
        # TODO: Data validation
        try:
            uid = interaction.user.id
            new_data = {
                "firstname": " ".join(x for x in self.name.value.split(" ") if x.istitle()),
                "lastname": " ".join(x for x in self.name.value.split(" ") if x.isupper()),
                "email": self.email.value,
                "github": self.github.value,
                "linkedin": self.linkedin.value,
                "discord": uid,
                "birthday": [int(x) for x in self.birthday.value.split("/", 3)]
            }
            all_data = [new_data if data.get("discord", None) == uid else data for data in load("info")]
            save("info", all_data)
            await interaction.response.send_message("Your profile has been updated successfuly.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong: {e}", ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, exception: Exception) -> None:
        await interaction.response.send_message(f"Error: {exception}", ephemeral=True)