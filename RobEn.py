# Work with Python 3.6
import discord
from discord.ext import commands

client = discord.Client()
TOKEN = "ODIyNTU0NzUzODg4Mjg4ODU1.YFT9zw.ifk8Q4GAd08Nz2H8BSFZTwMp_P8"

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
    
@client.event
async def on_voice_state_update(member, before, after):
    channel = client.get_channel("channel ID")
    if before.channel is None and after.channel is not None:
        embed = discord.Embed(
            description = f"{member.mention} joined voice channel",
            colour = discord.Colour.green()
        )
        embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
        embed.set_author(name=member, icon_url=member.avatar_url)
        await channel.send(embed=embed)
    else:
        embed = discord.Embed(
            description = f"{member.mention} left voice channel",
            colour = discord.Colour.red()
        )
        embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
        embed.set_author(name=member, icon_url=member.avatar_url)
        await channel.send(embed=embed)    

   
client.run(TOKEN)
