import discord
from discord.ext import commands
from config import TOKEN
import os
import importlib

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix="*", intents=intents)

async def load_files(folder, extension_type='cogs'):
    try:
        for filename in os.listdir(f"./cogs/{folder}"):
            if filename.endswith(".py") and not filename.startswith("__"):
                if extension_type == 'cogs':
                    # Carrega cogs (comandos e eventos)
                    await bot.load_extension(f"cogs.{folder}.{filename[:-3]}")
                elif extension_type == 'views':
                    # Carrega views
                    module_name = f"cogs.views.{filename[:-3]}"
                    module = importlib.import_module(module_name)
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, discord.ui.View) and attr is not discord.ui.View:
                            bot.add_view(attr())
        print(f"✅ {folder.capitalize()} carregados com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar os {folder.capitalize()}. Erro: {e}")

async def load_cogs():
    await load_files("commands")
    await load_files("events")
    await load_files("views", extension_type='views')

async def main():
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())