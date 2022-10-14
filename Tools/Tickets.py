import discord
import json
from Tools.Config import Config

with open("conf.json", "r") as f:
    config = Config(json.load(f))


class OpenMenu(discord.ui.View):
    interaction: discord.Interaction

    def __init__(self):
        super().__init__()
        self.value = None

    def is_ticket_exists(self, ticket_channel_name):
        existing_channel = discord.utils.get(self.interaction.guild.channels, name=ticket_channel_name)
        if existing_channel is None:
            return False
        else:
            return True

    @discord.ui.button(label=config.buttons["create_ticket"], style=discord.ButtonStyle.green)
    async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.interaction = interaction
        await self.create_ticket()

    async def create_ticket(self):
        guild = self.interaction.guild
        ticket_channel_name = 'ticket-' + self.interaction.user.name

        if self.is_ticket_exists(ticket_channel_name):
            await self.interaction.response.send_message(config.text["ticket_exists"], ephemeral=True)
            return

        category = discord.utils.get(self.interaction.guild.categories, name=self.interaction.channel.category.name)

        if self.interaction.user.guild_permissions.manage_channels:
            await guild.create_text_channel(name='{}'.format(ticket_channel_name), category=category)
            await self.interaction.response.send_message(config.text["ticket_created"], ephemeral=True)
            created_ticket = TicketSystem(self.interaction, self.interaction.user.name)
            await created_ticket.create_closing()


class CloseMenu(discord.ui.View):
    interaction: discord.Interaction

    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label=config.buttons["close_ticket"], style=discord.ButtonStyle.red)
    async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.interaction = interaction
        await self.close_ticket()

    async def close_ticket(self):
        await self.interaction.channel.send(config.text["closing_ticket"])
        await self.interaction.channel.delete()


class TicketSystem:
    interaction: discord.Interaction
    user_nickname: str

    def __init__(self, interaction, user_nickname):
        self.interaction = interaction
        self.user_nickname = user_nickname

    async def create_opening(self):
        await self.interaction.channel.send(config.text["create_ticket"], view=OpenMenu())

    async def create_closing(self):
        channel = discord.utils.get(self.interaction.guild.channels, name='ticket-' + self.interaction.user.name)
        await channel.send(config.text["close_ticket"], view=CloseMenu())
