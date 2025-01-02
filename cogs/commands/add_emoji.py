import discord
from discord.ext import commands
from emojis import *
import aiohttp

class AddEmojiCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description="Adiciona um emoji personalizado ao servidor atual.")
    async def add_emoji(self, interaction: discord.Interaction, emoji: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"{EMOJI_X} Você não tem permissão para usar este comando. É necessário ter permissão de administrador.", ephemeral=True)
            return

        if not interaction.guild:
            await interaction.response.send_message("Este comando deve ser executado em um servidor.", ephemeral=True)
            return

        if emoji.startswith('<:') and emoji.endswith('>'):
            emoji_id = emoji.split(':')[2].split('>')[0]
            emoji_name = emoji.split(':')[1]

            emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.png"

            async with aiohttp.ClientSession() as session:
                try:
                    # Faz o download da imagem do emoji
                    async with session.get(emoji_url) as response:
                        if response.status != 200:
                            await interaction.response.send_message(f"{EMOJI_X} Não consegui acessar a imagem do emoji.",ephemeral=True)
                            return
                        image_data = await response.read()

                    # Adiciona o emoji ao servidor
                    new_emoji = await interaction.guild.create_custom_emoji(name=emoji_name,image=image_data)
                    await interaction.response.send_message(f"{EMOJI_CHECK} Emoji adicionado com sucesso: {new_emoji}",ephemeral=True)

                except Exception as e:
                    await interaction.response.send_message(f"{EMOJI_X} Ocorreu um erro: {str(e)}",ephemeral=True)
        else:
            await interaction.response.send_message(f"{EMOJI_X} Por favor, forneça um emoji personalizado válido.",ephemeral=True)

async def setup(bot):
    await bot.add_cog(AddEmojiCommand(bot))
