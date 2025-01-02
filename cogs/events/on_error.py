import discord
from discord.ext import commands
import traceback
from emojis import EMOJI_ALERTA

class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_error(self, event_method, *args, **kwargs):
        """
        Captura erros gerais em eventos e loga no console.
        """
        print(f"❌ Um erro ocorreu no evento '{event_method}':")
        traceback.print_exc()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Captura erros em comandos e loga no console.
        """
        if isinstance(error, commands.CommandNotFound):
            # Ignora erros de comandos inexistentes
            return

        print(f"❌ Erro no comando '{ctx.command}':")
        traceback.print_exc()

        # Mensagem amigável para o usuário (opcional)
        await ctx.send(f"{EMOJI_ALERTA} Ocorreu um erro ao executar este comando.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
