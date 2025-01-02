import discord
from discord.ext import commands
import base64
import io
from emojis import *
from datetime import datetime, timedelta
import pytz
import mercadopago
from config import TOKEN_MP
from cogs.views.payment_view import PaymentView
import sqlite3

class FazerPixCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def registrar_cobranca(self, id_cliente, id_server, id_canal, id_msg, id_pagamento, data_limite):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO cobrancas (id_cliente, id_server, id_canal, id_msg, id_pagamento, data_limite) VALUES (?, ?, ?, ?, ?, ?)",
                (id_cliente, id_server, id_canal, id_msg, id_pagamento, data_limite)
            )
            conn.commit()
        except sqlite3.Error as e:
            print(f"Erro ao inserir dados no banco: {e}")
        finally:
            conn.close()

    @discord.app_commands.command(description="「Geral」Fazer um pagamento via PIX")
    @discord.app_commands.describe(valor="Valor do pagamento em reais (mínimo R$ 1,00)")
    async def fazer_pixpy(self, interaction: discord.Interaction, valor: float):
        if valor < 1:
            await interaction.response.send_message(f"{EMOJI_X} O valor inserido deve ser maior do que 1.", ephemeral=True)
            return
        
        valor_formatado = f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

        sdk = mercadopago.SDK(TOKEN_MP)
        idempotency_key = str(datetime.now().timestamp())
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': idempotency_key
        }
        payment_data = {
            "transaction_amount": valor,
            "description": f"Hospedagem Mensal - R$ {valor_formatado} [{interaction.user.name} | {interaction.user.id}]",
            "payment_method_id": "pix",
            "payer": {
                "email": "email@email.com.br",
                "first_name": f"{interaction.user.name}",
                "last_name": f"{interaction.user.id}",
                "identification": {
                    "type": "CUSTOM_ID",
                    "number": f"{interaction.user.id}"
                }
            }
        }
        payment_response = sdk.payment().create(payment_data, request_options)
        response = payment_response['response']

        payment_id = response['id']
        qrcode = response['point_of_interaction']['transaction_data']['qr_code']
        ticket_url = response['point_of_interaction']['transaction_data']['ticket_url']
        qr_code_base64 = response['point_of_interaction']['transaction_data']['qr_code_base64']

        image_data = base64.b64decode(qr_code_base64)
        image_file = io.BytesIO(image_data)
        image_file.seek(0)

        # armazenando dados da cobrança
        fuso_brasilia = pytz.timezone('America/Sao_Paulo')
        data_hora_brasilia = datetime.now(fuso_brasilia)
        data_hora_acrescentada = data_hora_brasilia + timedelta(minutes=5)
        data_hora_formatada = data_hora_acrescentada.strftime("%d/%m/%Y %H:%M")

        embed_pix = discord.Embed(title=f"{EMOJI_LOADING} AGUARDANDO PAGAMENTO")
        embed_pix.color = 0xff6200
        embed_pix.add_field(name="💵 Valor:", value=f"R$ {valor_formatado}", inline=False)
        embed_pix.add_field(name="💠 QRCode:", value=f"```{qrcode}```", inline=False)
        embed_pix.set_image(url="attachment://qr_code.png")
        embed_pix.set_footer(text=f"Expira em: 5 minutos. | {data_hora_formatada}")

        # Envia a mensagem e armazena o ID da mensagem real
        msg = await interaction.response.send_message(
            f"{interaction.user.mention}",
            embed=embed_pix,
            file=discord.File(image_file, filename="qr_code.png"),
            view=PaymentView(url=ticket_url)
        )
        msg_obj = await interaction.original_response()

        self.registrar_cobranca(
            id_cliente=interaction.user.id,
            id_server=interaction.guild.id if interaction.guild else 0,
            id_canal=interaction.channel.id,
            id_msg=msg_obj.id,
            id_pagamento=payment_id,
            data_limite=data_hora_formatada
        )

async def setup(bot):
    await bot.add_cog(FazerPixCommand(bot))
