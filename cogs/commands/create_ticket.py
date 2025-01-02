import discord
from discord.ext import commands
from discord.utils import get
import sqlite3
import emojis

# Configuração do banco de dados SQLite
def init_db():
    conn = sqlite3.connect("database.db")  # Conectando ao banco de dados existente
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket (
        user_id TEXT,
        server_id TEXT,
        channel_id TEXT
    )
    """)
    conn.commit()
    return conn, cursor

conn, cursor = init_db()

class CreateTicket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name="create_ticket", description="「Adm」Crie o sistema de ticket para o seu servidor.")
    async def create_ticket(self, interaction: discord.Interaction):
        # Verifica permissão
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                f"{EMOJI_X} Você não tem permissão para usar este comando.", ephemeral=True
            )
            return

        # Verifica ou cria a categoria
        category = get(interaction.guild.categories, name="「🎫」ticket")
        if category is None:
            category = await interaction.guild.create_category("「🎫」ticket")

            # Cria o canal de informações na categoria
            info_channel = await category.create_text_channel("📜-informações")
            await info_channel.set_permissions(
                interaction.guild.default_role,
                view_channel=True,  # Permite visualizar o canal
                send_messages=False  # Bloqueia envio de mensagens
            )

            # Mensagem ephemera notificando que o canal foi criado
            await interaction.response.send_message(
                f"✅ Sistema de ticket configurado com sucesso! Canal {info_channel.mention} criado.",
                ephemeral=True
            )

            # Envia a mensagem com as opções de ticket no canal criado
            embed = discord.Embed(
                title="Sistema de Ticket",
                description="Selecione uma das opções abaixo para criar um ticket:",
                color=discord.Color.blue()
            )

            # Menu de seleção
            class TicketMenu(discord.ui.View):
                def __init__(self):
                    super().__init__(timeout=None)
                    self.select = discord.ui.Select(
                        placeholder="Escolha uma opção...",
                        options=[
                            discord.SelectOption(label="Suporte", value="suporte", emoji="🛠️"),
                            discord.SelectOption(label="Comprar", value="comprar", emoji="💳"),
                            discord.SelectOption(label="Resetar a opção", value="reset", emoji="🔄")
                        ]
                    )
                    self.select.callback = self.select_callback
                    self.add_item(self.select)

                async def select_callback(self, interaction: discord.Interaction):
                    option = self.select.values[0]

                    if option == "reset":
                        await interaction.response.send_message(
                            "🔄 Opção redefinida. Escolha novamente no menu abaixo.",
                            ephemeral=True
                        )
                        return

                    cursor.execute(
                        "SELECT channel_id FROM ticket WHERE user_id = ? AND server_id = ?",
                        (str(interaction.user.id), str(interaction.guild.id))
                    )
                    result = cursor.fetchone()

                    if result:
                        # Se já existe um ticket aberto
                        channel_id = result[0]
                        channel = interaction.guild.get_channel(int(channel_id))
                        if channel:
                            await interaction.response.send_message(
                                f"{EMOJI_X} Você já possui um ticket aberto: {channel.mention}.", ephemeral=True
                            )
                        else:
                            # Caso o canal registrado no banco não exista mais, remover do banco
                            cursor.execute(
                                "DELETE FROM ticket WHERE user_id = ? AND server_id = ?",
                                (str(interaction.user.id), str(interaction.guild.id))
                            )
                            conn.commit()
                            await interaction.response.send_message(
                                f"{EMOJI_X} O canal do seu ticket foi deletado. Tente criar outro.", ephemeral=True
                            )
                        return

                    # Criar o canal do ticket
                    channel = await category.create_text_channel(f"🎫-{option}_{interaction.user.name}")
                    await channel.set_permissions(interaction.guild.default_role, view_channel=False)
                    await channel.set_permissions(interaction.user, view_channel=True, send_messages=True)

                    cursor.execute(
                        "INSERT INTO ticket (user_id, server_id, channel_id) VALUES (?, ?, ?)",
                        (str(interaction.user.id), str(interaction.guild.id), str(channel.id))
                    )
                    conn.commit()

                    await channel.send(embed=discord.Embed(
                        title="Ticket Criado",
                        description=f"{interaction.user.mention}, seu ticket foi criado com sucesso!",
                        color=discord.Color.green()
                    ))
                    await interaction.response.send_message(
                        f"✅ Ticket criado: {channel.mention}.", ephemeral=True
                    )

            await info_channel.send(embed=embed, view=TicketMenu())

        else:
            await interaction.response.send_message(
                f"{EMOJI_X} O sistema de tickets já está configurado neste servidor.", ephemeral=True
            )

async def setup(bot):
    await bot.add_cog(CreateTicket(bot))
