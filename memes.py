from discord.ext import tasks
from assets import client,colors,reddit
import random
from discord import message,Embed



@tasks.loop(hours = 12)
async def send_memes():
    Channel = client.get_channel(807937662899847188)
    all_subs = []
    subreddit = reddit.subreddit("ProgrammerHumor")
    top = subreddit.hot(limit=50)
    for submission in top:
        all_subs.append(submission)
    random_sub = random.choice(all_subs)
    name = random_sub.title
    url = random_sub.url
    embed = Embed(title=name, colour = random.choice(colors))
    embed.set_image(url=url)
    await Channel.send(embed=embed)



async def SendMeme(message):
    all_subs = []
    subreddit = reddit.subreddit("ProgrammerHumor")
    top = subreddit.hot(limit=50)
    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    embed = Embed(title=name, colour = random.choice(colors))
    embed.set_image(url=url)
    await message.channel.send(embed=embed)
