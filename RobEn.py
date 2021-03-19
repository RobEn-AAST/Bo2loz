# Work with Python 3.6
import discord
from discord.ext import commands

TOKEN = "ODIyNTU0NzUzODg4Mjg4ODU1.YFT9zw.ifk8Q4GAd08Nz2H8BSFZTwMp_P8"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
