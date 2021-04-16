# Work with Python 3.6
from operator import truth
from time import time
import discord
from discord import message
from discord import guild
from discord import member
from discord import channel
from discord.errors import NoMoreItems
from discord.ext import commands
from discord.ext.commands.errors import NoPrivateMessage
from discord.member import Member
from datetime import timedelta,datetime
from discord.ext import tasks
import re
import random
import praw



TOKEN = "BOT TOKEN"


class meeting :
    def __init__(self, member_name):

        self.admin = member_name
        self.time = None
        self.location = None
        self.topic= None
        self.active = False
        self.not_confirmed = []
        self.meeting_id = None
        self.meeting_attendance = []
        self.started = False
        return

intents = discord.Intents.default()
intents.members = True

client  = discord.Client(intents = intents)
colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400, 0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]

Keywords = {"create":{"create","new","construct","generate","form","establish"},
            "meeting": {"meeting","gathering","appointment","party","interview"},
            "days": {"satur","sun","mon","tues","wednes","thurs"},
            "modify": {"change","modify","postpone","reschedule","re-schedule","re schedule"},
            "remove": {"cancel","remove","shutdown","delete","drop"}
}

reddit = praw.Reddit(client_id="client ID",
                     client_secret="client secret",
                     username = "reddit username",
                     password = "reddit password",
                     user_agent="user agent",
                     check_for_async=False)



chats = {}

meetings = {}

def word_to_date(Time,day):
    day = day.replace(" ", "")
    time = re.findall("[0-9][0-2]*:[0-9]{2}",Time)[0]
    state = re.findall("[p|a|P|A]",Time)[0]
    hour,minute = map(int,time.split(':'))
    if state == "P" or state == "p":
        hour += 12
    today = datetime.today()
    while True:
        if today.strftime('%A').lower() != day:
            today += timedelta(days=1)
        else:
            break
    return today.replace(hour= hour,minute=minute)

def Update_Chat(member_name,message):
    global chats
    if member_name in chats.keys():
        chats[member_name] = message
    else:
        chats.update({ member_name : message })

def Logic_Handling(value,member_name):
    global meetings
    global chats
    last_message = chats[member_name]
    if member_name not in meetings.keys():
        meetings[member_name] = []
    if value:
        if last_message == member_name +" Do you wish to make a new meeting ?":
            meetings[member_name].append((datetime.now(),meeting(member_name= member_name)))
            bo2loz_message = member_name + ''' please give me the meeting information in one message separated by commas...meeting information are
1 - meeting day
2 - meeting time >> ex: (2:30 pm)
3 - meeting location
4 - meeting topic

example >> day : wednesday,time : 3:40 pm,location : nasr city, topic : 2a3da ray2a

'''
            flag = False
            for x in meetings[member_name]:
                if x[1].topic == None and flag == False:
                    flag = True
                elif x[1].topic == None and flag == True:
                    bo2loz_message = member_name + " You cannot make a new meeting until you finish setting up the previous meeting"
    else:
        bo2loz_message = "okai :pleading_face::pleading_face::pleading_face:"
    embed = discord.Embed(
                            description = bo2loz_message,
                            colour = discord.Colour.green()
                        )
    Update_Chat(member_name= member_name, message= bo2loz_message)
    return embed,bo2loz_message




@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    remind_members.start()
    start_meetings.start()
    send_memes.start()

@client.event
async def on_member_join(member):
    if member.bot:
        return
    role = member.guild.get_role(822598861402013707)
    await member.add_roles(role)
    role = member.guild.get_role(822599244841091092)
    await member.add_roles(role)
    await member.create_dm()
    welcome_message = 'Hi ' + member.name +''' , welcome to Robben AI team !!!\nRules :
- No spamming
- Text only in the appropriate channel
- Confirm on meetings in the meetings plans channel by reacting to meeting message with a :thumbsup:
- Keep notifications on at all times
- Regularly check the server for announcements and meeting plans
- Share memes as if it's your job
- If you are new to discord please check our toturial on youtube
        https://www.youtube.com/watch?v=09y5ydmNwGA
- If wish to review our rules at any time, they are available on the roles channel
        '''
    await member.dm_channel.send(welcome_message)
    Update_Chat(member_name= member.name,message = welcome_message)

@tasks.loop(hours=24)
async def remind_members():
    members = client.get_all_members()
    for x in members:
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if (y[1].time - datetime.today()).days + 1 < 2:
                    mem = client.get_all_members()
                    for z in mem:
                        if z.name  in y[1].not_confirmed:
                            message = "The is a meeting shceduled on " + y[1].day + "  " + y[1].time + " at" + y[1].location + "\nplease open the meetings channel and check it out\nif you cannot arrive please send me a message containing the word excuse and your excuse\n\nalways glad to help :nerd: :nerd: :nerd:"
                            channel = await z.create_dm()
                            await channel.send(message)

@tasks.loop(minutes = 1)
async def start_meetings():
    members = (x for x in client.get_all_members())
    for x in members:
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if y[1].time >= datetime.now() and not y[1].started:
                    y[1].started = True
                    channel = client.get_channel(822588656627089500)
                    await channel.send("Hello every one...Bo2loz here,\nThe " + y[1].topic + " meeting will start now so please enter the voice channel now.\nGood luck Team !!!")


@client.event
async def on_voice_state_update(member, before, after):
    role = member.guild.get_role(822598861402013707)
    guild = client.get_guild(822565883557183538)
    memberList = []
    for user in guild.members:
        if role in user.roles:
            memberList.append(user.mention)
    for x in client.get_all_members():
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if y[1].active == True:
                    channel = client.get_channel(y[1].meeting_id)
                    if before.channel is None and after.channel is not None and role in member.roles:
                        if after.channel.id == y[1].meeting_id:
                            if member.mention in memberList:
                                memberList.remove(member.mention)
                                embed = discord.Embed(
                                    description = f"{member.mention} joined  " + y[1].topic + " meeting voice channel",
                                    colour = discord.Colour.green()
                                )
                                embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
                                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                                embed.add_field(name="Missing members", value=", ".join(memberList), inline=True)
                                await client.get_channel(822588656627089500).send(embed=embed)


                    elif before.channel is not None and after.channel is None and role in member.roles:
                        if before.channel.id == y[1].meeting_id:
                            memberList.append(member.mention)
                            embed = discord.Embed(
                            description = f"{member.mention} left " + y[1].topic + " meeting voice channel",
                            colour = discord.Colour.red()
                            )
                            embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
                            embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                            await client.get_channel(822588656627089500).send(embed=embed)


@client.event
async def on_message(message):
    if message.author.bot:
        return
    global chats
    global meetings
    if message.channel == client.get_channel(822890915906846720):
        return
    if "bo2loz" in message.content.lower():
        if "yes" in message.content.lower() or "no" in message.content.lower() :
            embed,bo2loz_message = Logic_Handling(True if "yes" in message.content.lower() else False,message.author.name)
        else:
            if any(x in message.content.lower() for x in Keywords.get("create")) and any(x in message.content.lower() for x in Keywords.get("meeting")):
                bo2loz_message = message.author.name +" Do you wish to make a new meeting ?"
                embed = discord.Embed(
                                    description = bo2loz_message,
                                    colour = discord.Colour.green()
                                )
            elif "time" in message.content.lower() and "location" in message.content.lower() and "day" in message.content.lower() and "topic" in message.content.lower():
                    time = re.findall("[Tt]ime\s*:\s*[0-9][0-2]*:[0-9]{2}\s*[A|a|P|p][m|M],*",message.content.lower())[0]
                    day = re.findall("[Dd]ay\s*:\s*\w+day\s*,*",message.content.lower())[0]
                    location = re.findall("[Ll]ocation\s*:.+,*",message.content.lower())[0]
                    topic = re.findall("[Tt]opic\s*:.+,*",message.content.lower())[0]
                    time = time[time.index(':') + 1:time.index(',') if ',' in time else len(time)].strip()
                    day = day[day.index(':') + 1:day.index(',')  if ',' in day else len(day)].strip()
                    location = location[location.index(':') + 1:location.index(',') if ',' in location else len(location)].strip()
                    topic = topic[topic.index(':') + 1:topic.index(',') if ',' in topic else len(topic)].strip()
                    all_members = client.get_all_members()
                    for x in meetings[message.author.name]:
                        if x[1].active == False:
                            x[1].time = word_to_date(time,day)
                            x[1].topic = topic
                            x[1].active = True
                            await client.get_guild(822565883557183538).create_voice_channel(name = topic + " voice meeting")
                            for y in client.get_all_channels():
                                if y.name == topic + " voice meeting":
                                    x[1].meeting_id = y.id
                            for y in all_members:
                                if not y.bot and y.name != message.author.name :
                                    x[1].not_confirmed.append(y.name)
                            break

                    channel = client.get_channel(822890915906846720)
                    await channel.send("Hello every one Bo2loz here\n" + message.author.name + " Just created a meeting!!!\n" +"meeting location : " + location + "\nmeeting time : " + day + "   " + time + "\nmeeting topic :" + topic + "\n\nif you have any excuses please send me a message containing the word (excuse) and your excuse\n\nalways glad to help :nerd: :nerd: :nerd:")
                    bo2loz_message = "meeting made successfully ya ba4a !!!\n your voice channel is ready"
            else:
                bo2loz_message = "3ayez eh ?????"
            embed = discord.Embed(
                                description = bo2loz_message,
                                colour = discord.Colour.green()
                            )
        Update_Chat(member_name= message.author.name, message= bo2loz_message)
        await message.channel.send(embed = embed)
    if message.content == "!memes":
        all_subs = []
        subreddit = reddit.subreddit("ProgrammerHumor")
        top = subreddit.hot(limit=50)
        for submission in top:
            all_subs.append(submission)

        random_sub = random.choice(all_subs)

        name = random_sub.title
        url = random_sub.url

        embed = discord.Embed(title=name, colour = random.choice(colors))
        embed.set_image(url=url)
        await message.channel.send(embed=embed)

@tasks.loop(hours = 12)
async def send_memes():
    client.get_channel(CHANNEL ID HERE)
    all_subs = []
    subreddit = reddit.subreddit("ProgrammerHumor")
    top = subreddit.hot(limit=50)
    for submission in top:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    embed = discord.Embed(title=name, colour = random.choice(colors))
    embed.set_image(url=url)
    await message.channel.send(embed=embed)


client.run(TOKEN)
