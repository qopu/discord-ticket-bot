import discord
import json
from Tools.Config import Config

with open("conf.json", "r") as f:
    config = Config(json.load(f))


class ButtonMenu(discord.ui.View):
    interaction: discord.Interaction

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label=config.buttons["create_ticket"], style=discord.ButtonStyle.green)
    async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.interaction = interaction
        await self.create_ticket()

    async def create_ticket(self):
        guild = self.interaction.guild
        ticket_channel_name = 'ticket-' + self.interaction.user.name

        category = discord.utils.get(self.interaction.guild.categories, name=self.interaction.channel.category.name)

        await guild.create_text_channel(name='{}'.format(ticket_channel_name), category=category)
        await self.interaction.response.send_message(config.text["ticket_created"], ephemeral=True)


class TicketSystem:
    interaction: discord.Interaction
    user_nickname: str

    def __init__(self, interaction, user_nickname):
        self.interaction = interaction
        self.user_nickname = user_nickname

    async def create(self):
        await self.interaction.channel.send(config.text["creating_ticket_system"], view=ButtonMenu())
