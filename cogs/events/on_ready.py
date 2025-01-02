import discord
from discord.ext import commands
from emojis import *

class OnReadyEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.tree.sync()
        await self.bot.change_presence(status=discord.Status.idle, activity=discord.CustomActivity(name="⚠️ Em manutenção..."))
        print("✅ Bot inicializado com sucesso!")

async def setup(bot):
    await bot.add_cog(OnReadyEvent(bot))