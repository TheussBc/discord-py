import discord

class PaymentView(discord.ui.View):
    def __init__(self, url=None):
        super().__init__(timeout=None)
        if url:
            self.add_item(discord.ui.Button(label="URL de Pagamento", url=url, style=discord.ButtonStyle.link))

    @discord.ui.button(label="Copiar QR Code", style=discord.ButtonStyle.secondary, custom_id="show_qrcode")
    async def show_qrcode(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.message.embeds:
            embed = interaction.message.embeds[0]
            if len(embed.fields) > 1:
                qrcode_field = embed.fields[1].value
                qr_code64 = qrcode_field.strip("`")
                
                await interaction.response.send_message(qr_code64, ephemeral=True)
                return
        await interaction.response.send_message("QR Code não disponível.", ephemeral=True)
