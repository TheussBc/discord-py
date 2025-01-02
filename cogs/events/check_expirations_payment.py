import discord
from discord.ext import commands, tasks
from datetime import datetime
import sqlite3
import pytz
from emojis import EMOJI_X
import mercadopago
from config import TOKEN_MP

class CheckExpirationsPayment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_expirations_task.start()

    def cog_unload(self):
        self.check_expirations_task.cancel()

    async def cancelar_pagamento(self, id_payment):
        try:
            sdk = mercadopago.SDK(TOKEN_MP)
            sdk.payment().update(id_payment, {"status": "cancelled"})
        except Exception as e:
            print(f"Erro ao cancelar o pagamento: {e}")

    @tasks.loop(seconds=5)
    async def check_expirations_task(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        fuso_brasilia = pytz.timezone('America/Sao_Paulo')
        data_hora_atual = datetime.now(fuso_brasilia).strftime("%d/%m/%Y %H:%M")

        # Busca cobranças expiradas
        cursor.execute("SELECT id_cliente, id_server, id_canal, id_msg, id_pagamento FROM cobrancas WHERE data_limite <= ?", (data_hora_atual,))
        expiradas = cursor.fetchall()

        for id_cliente, id_server, id_canal, id_msg, id_pagamento in expiradas:
            try:
                user = await self.bot.fetch_user(int(id_cliente))
                username = user.name
                guild = self.bot.get_guild(int(id_server))
                if not guild:
                    print(f"Servidor com ID {id_server} não encontrado.")
                    continue

                channel = guild.get_channel(int(id_canal))
                if not channel:
                    print(f"Canal com ID {id_canal} não encontrado no servidor {id_server}.")
                    continue

                msg = await channel.fetch_message(int(id_msg))

                # Atualiza a mensagem com o embed de cobrança expirada
                embed_expirado = discord.Embed(
                    title=f"{EMOJI_X} COBRANÇA EXPIRADA",
                    description=f"{username}, esta cobrança expirou e não é mais válida.",
                    color=discord.Color.red()
                )

                try:
                    await msg.edit(embed=embed_expirado, attachments=[], view=None)
                except Exception as e:
                    print(f"Erro ao editar mensagem: {e}")
                    
            except discord.NotFound:
                print(f"Mensagem com ID {id_msg} não encontrada no canal {id_canal}.")
            except Exception as e:
                print(f"Erro ao editar mensagem com ID {id_msg} no canal {id_canal}: {e}")
            
            await self.cancelar_pagamento(id_pagamento)

        # Remove cobranças expiradas do banco de dados
        cursor.execute("DELETE FROM cobrancas WHERE data_limite <= ?", (data_hora_atual,))
        conn.commit()
        conn.close()

    @check_expirations_task.before_loop
    async def before_check_expirations(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(CheckExpirationsPayment(bot))