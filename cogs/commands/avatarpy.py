import discord
import datetime
from discord.ext import commands

class AvatarCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description="「Geral」Veja o avatar de um usuário")
    @discord.app_commands.choices(ephemeral_opcao=[
        discord.app_commands.Choice(name="Ativar", value="ativo"),
        discord.app_commands.Choice(name="Desativar", value="desativo")
    ])
    async def avatar(self, interaction: discord.Interaction, ephemeral_opcao: discord.app_commands.Choice[str], usuario: discord.User = None):
        embed = discord.Embed(
            color=discord.Color.from_str("#73ff98"),
            timestamp=datetime.datetime.now()
        )

        if usuario is not None:
            embed.set_author(name=usuario.name, icon_url=usuario.avatar.url)
            embed.set_image(url=usuario.avatar.url)
        else:
            embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
            embed.set_image(url=interaction.user.avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=(ephemeral_opcao.value == "ativo"))

async def setup(bot):
    await bot.add_cog(AvatarCommand(bot))
