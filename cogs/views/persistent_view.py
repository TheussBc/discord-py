import discord

class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(HelloButton())
        self.add_item(GoodbyeButton())

class HelloButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Say Hello", style=discord.ButtonStyle.green, custom_id="hello_button")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello!", ephemeral=True)

class GoodbyeButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Dizer Adeus", style=discord.ButtonStyle.red, custom_id="goodbye_button")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("Adeus!", ephemeral=True)
