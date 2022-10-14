import discord
import time
import json
from discord import app_commands
from pathlib import Path

from Tools.Tickets import TicketSystem
from Tools.Config import Config

TOKEN = Path("token.txt").read_text()  # file gitignored

with open("conf.json", "r") as f:
    config = Config(json.load(f))


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


@commands.command(name="create_ticket_system", description=config.commands["create_ticket_system"])
async def self(ctx: discord.Interaction):
    await ctx.response.send_message(config.text["creating_ticket_system"])
    time.sleep(2)
    await ctx.channel.purge(limit=1)

    ticket = TicketSystem(interaction=ctx, user_nickname=ctx.user.name)
    await ticket.create_opening()


@commands.command(name="clear", description=config.commands["clear"])
async def test(ctx: discord.Interaction, amount: str):
    try:
        if not 0 < int(amount) < 1000:
            await ctx.response.send_message(config.text["value_big_or_small"])
            return
        amount = int(amount)
        await ctx.response.send_message(config.text["deleting"] + f" {amount} " + config.text["messages"])
    except ValueError:
        await ctx.response.send_message(config.text["incorrect_value"])
        return

    await ctx.channel.purge(limit=amount)


client.run(TOKEN)
