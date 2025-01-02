import discord
from discord.ext import commands, tasks
import sqlite3
from config import TOKEN_MP
import mercadopago
from emojis import EMOJI_CHECK

class CheckPayments(commands.Cog):
    def __init__(self, bot, sdk):
        self.bot = bot
        self.sdk = sdk
        self.check_payments_task.start()

    def cog_unload(self):
        self.check_payments_task.cancel()

    @tasks.loop(seconds=5)
    async def check_payments_task(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id_pagamento, id_cliente, id_server, id_canal, id_msg FROM cobrancas")
        pagamentos = cursor.fetchall()

        for id_pagamento, id_cliente, id_server, id_canal, id_msg in pagamentos:
            payment_info = self.sdk.payment().get(id_pagamento)
            status = payment_info['response'].get('status')

            if status == "approved":
                try:
                    user = await self.bot.fetch_user(int(id_cliente))
                    username = user.name
                    guild = self.bot.get_guild(int(id_server))
                    channel = guild.get_channel(int(id_canal))
                    msg = await channel.fetch_message(int(id_msg))
            
                    embed_confirmado = discord.Embed(
                        title=F"{EMOJI_CHECK} PAGAMENTO CONFIRMADO",
                        description=f"{username}, seu pagamento foi confirmado com sucesso!",
                        color=discord.Color.green()
                    )
                    embed_confirmado.set_footer(text="Obrigado pela sua contribuição!")

                    await msg.edit(embed=embed_confirmado, attachments=[], view=None)

                    # Remover do banco de dados
                    cursor.execute("DELETE FROM cobrancas WHERE id_pagamento = ?", (id_pagamento,))
                    conn.commit()

                except Exception as e:
                    print(f"Erro ao editar mensagem ou excluir do banco: {e}")

        conn.close()

    @check_payments_task.before_loop
    async def before_check_payments(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    sdk = mercadopago.SDK(TOKEN_MP)
    await bot.add_cog(CheckPayments(bot, sdk))
