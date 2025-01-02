import discord
from discord.ext import commands

class IdiomaCommand(commands.Cog):
    def __init__(self, bot):
            self.bot = bot

    @discord.app_commands.command(name="idioma", description="「Geral」Mostra o idioma configurado do usuário no Discord")
    async def idioma(self, interaction: discord.Interaction):
        user_locale = interaction.locale
        await interaction.response.send_message(f"Seu idioma configurado no Discord é: `{user_locale}`")

async def setup(bot):
    await bot.add_cog(IdiomaCommand(bot))