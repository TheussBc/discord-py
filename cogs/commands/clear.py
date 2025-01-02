import discord
from discord.ext import commands
from emojis import *

class ClearCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description="Limpa até 100 mensagens do canal.")
    async def clear(self, interaction: discord.Interaction, quantidade: int):
        if not (interaction.user.guild_permissions.manage_messages or interaction.user.id == interaction.guild.owner_id):
            await interaction.response.send_message(f"{EMOJI_X} Você não tem permissão para usar este comando.", ephemeral=True)
            return
        
        if quantidade < 1 or quantidade > 100:
            await interaction.response.send_message(f"{EMOJI_ALERTA} Por favor, escolha um número entre 1 e 100.", ephemeral=True)
            return
        
        await interaction.response.send_message(f"{EMOJI_LOADING} Limpando mensagens, por favor aguarde...", ephemeral=True)

        deleted_messages = await interaction.channel.purge(limit=quantidade)

        if len(deleted_messages) == 0:
            await interaction.edit_original_response(content=f"{EMOJI_X} Não há mensagens para deletar.")
        else:
            await interaction.edit_original_response(content=f"{EMOJI_CHECK} {len(deleted_messages)} mensagens foram excluídas.")

async def setup(bot):
    await bot.add_cog(ClearCommand(bot))