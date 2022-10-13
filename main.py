import discord
import time
from discord import app_commands
from pathlib import Path

from Tools.Tickets import TicketSystem

TOKEN = Path("token.txt").read_text()  # file gitignored


class Client(discord.Client):
    async def on_ready(self):
        await self.wait_until_ready()
        await commands.sync()
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')


intents = discord.Intents.default()

client = Client(intents=intents)

commands = app_commands.CommandTree(client)


@commands.command(name="create_ticket_system", description="Creates a ticket system and sends initial message")
async def self(ctx: discord.Interaction):
    await ctx.response.send_message("Creating a ticket system...")
    time.sleep(2)
    await ctx.channel.purge(limit=1)

    ticket = TicketSystem(interaction=ctx, user_nickname=ctx.user.name)
    await ticket.create()


@commands.command(name="clear", description="Deletes specified amount of messages above")
async def test(ctx: discord.Interaction, amount: str):
    try:
        if not 0 < int(amount) < 1000:
            await ctx.response.send_message("Value has to be **more than 1** and **less than 1000**")
            return
        amount = int(amount)
        await ctx.response.send_message(f"Deleting {amount} messages")
    except ValueError:
        await ctx.response.send_message("Incorrect value entered. Amount **must be a digit**")
        return

    await ctx.channel.purge(limit=amount)


client.run(TOKEN)
