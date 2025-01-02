from discord.ext import commands
from emojis import *

class OnCommandErrorEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(ctx, error):
        if isinstance(error, commands.CommandNotFound):
            # Se o comando não for encontrado, exibe uma mensagem específica
            print(f"❌ Comando '{ctx.command}' não encontrado.")
        elif isinstance(error, commands.MissingRequiredArgument):
            # Se faltar um argumento obrigatório, exibe uma mensagem específica
            print(f"❌ Argumentos faltando para o comando '{ctx.command}'. Erro: {error}")
        elif isinstance(error, commands.BadArgument):
            # Se houver um argumento inválido, exibe uma mensagem específica
            print(f"❌ Argumento inválido no comando '{ctx.command}'. Erro: {error}")
        else:
            # Para outros tipos de erro, exibe a mensagem geral
            print(f"❌ Erro ao executar o comando '{ctx.command}': {error}")

async def setup(bot):
    await bot.add_cog(OnCommandErrorEvent(bot))