from discord.ext import commands
from cogs.views.persistent_view import PersistentView

class ButtonsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_view(PersistentView())

    @commands.command(name="buttons")
    async def buttons(self, ctx):
        await ctx.send("Aqui estão os botões:", view=PersistentView())

async def setup(bot):
    await bot.add_cog(ButtonsCommand(bot))
