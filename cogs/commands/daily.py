import discord
from discord.ext import commands
from emojis import *
import sqlite3
from datetime import datetime
import pytz

class DailyCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(description='「Geral」Colete seu saldo diário')
    async def daily(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT data_daily, saldo FROM daily WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        
        fuso_brasilia = pytz.timezone('America/Sao_Paulo')
        data_hora_brasilia = datetime.now(fuso_brasilia)
        data_formatada = data_hora_brasilia.strftime("%d/%m/%Y")

        if not result:
            cursor.execute("INSERT INTO daily (id, data_daily, saldo) VALUES (?, ?, 5)", (user_id, data_formatada))
            conn.commit()
            await interaction.response.send_message(f"{EMOJI_CHECK} Saldo diário coletado com sucesso. Seu saldo atual é de R$ 5,00", ephemeral=True)
        elif result[0] == data_formatada:
            await interaction.response.send_message(f"{EMOJI_X} Você já coletou o saldo diário de hoje.", ephemeral=True)
        else:
            saldo = result[1]
            novo_saldo = saldo + 5
            saldo_formatado = f"{novo_saldo:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            cursor.execute("UPDATE daily SET data_daily = ?, saldo = ? WHERE id = ?", (data_formatada,novo_saldo, user_id))
            conn.commit()
            await interaction.response.send_message(f"{EMOJI_CHECK} Saldo diário coletado com sucesso! Seu novo saldo é de R$ {saldo_formatado}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(DailyCommand(bot))