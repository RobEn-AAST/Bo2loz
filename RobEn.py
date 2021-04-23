# Work with Python 3.6
import discord
from assets import update_config,Update_Chat
from assets import channels,client,chats,meetings,Keywords,standard_messages
from assets import BOT_TOKEN,meeting
from meetings import MakeNewMeeting,remind_members,start_meetings
from memes import send_memes,SendMeme


def Logic_Handling(value,member_name):
    global meetings
    global chats
    last_message = chats[member_name]
    if member_name not in meetings.keys():
        meetings[member_name] = []
    if value:
        if last_message == member_name +" Do you wish to make a new meeting ?":
            meetings[member_name].append(meeting(member_name))
            bo2loz_message = member_name + standard_messages["new meeting info"]
            flag = False
            for x in meetings[member_name]:
                if x.topic == None and flag == False:
                    flag = True
                elif x.topic == None and flag == True:
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
    for channel in client.get_all_channels():
        if channel.type == discord.ChannelType.text:
            channels["Text"][channel.name] = channel.id
        elif channel.type == discord.ChannelType.voice:
            channels["Audio"][channel.name] = channel.id
    remind_members.start()
    start_meetings.start()
    update_config.start()
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
    welcome_message = 'Hi ' + member.name + standard_messages["welcome to robben"]
    await member.dm_channel.send(welcome_message)
    Update_Chat(member_name= member.name,message = welcome_message)


@client.event
async def on_message(message):
    if message.author.bot or message.channel.id != message.author.dm_channel.id:
        return
    global chats
    global meetings
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
            await MakeNewMeeting(message)
            return
        else:
            bo2loz_message = "Can I help you `:eyes: `"
            embed = discord.Embed(
                            description = bo2loz_message,
                            colour = discord.Colour.green()
                        )
    Update_Chat(member_name= message.author.name, message= bo2loz_message)
    await message.channel.send(embed = embed)
    if message.content == "!memes":
        await SendMeme(message)


client.run(BOT_TOKEN)
