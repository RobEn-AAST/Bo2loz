# Work with Python 3.6
import discord
from assets import update_config,Update_Chat
from assets import channels,client,chats,meetings,Keywords,standard_messages,SERVER_ID
from assets import BOT_TOKEN,meeting
from meetings import MakeNewMeeting,remind_members,start_meetings,ModifyMeeting,CancelMeeting,ConfirmMeeting,ExcuseMeeting
from memes import send_memes,SendMeme


def Logic_Handling(value,member_name,member_id):
    global meetings
    global chats
    last_message = chats[member_name]
    if member_name not in meetings.keys():
        meetings[member_name] = []
    if value:
        if last_message == member_name +" Do you wish to make a new meeting ?":
            bo2loz_message = member_name + standard_messages["new meeting info"]
            flag = False
            for x in meetings[member_name]:
                if x.topic == None and flag == False:
                    flag = True
                elif x.topic == None and flag == True:
                    bo2loz_message = member_name + " You cannot make a new meeting until you finish setting up the previous meeting"
                    return
            meetings[member_name].append(meeting(member_id))
        elif last_message == member_name +" Do you wish to modify a meeting ?":
            bo2loz_message = member_name + standard_messages["edit meeting info"]
        elif last_message == member_name + " Do you wish to cancel a meeting ?":
             bo2loz_message = member_name + "please enter meeting id (example >> id : 123456789)"
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
    role = member.guild.get_role(809810876084781076)
    await member.add_roles(role)
    role = member.guild.get_role(807682737649614861)
    await member.add_roles(role)
    await member.create_dm()
    welcome_message = 'Hi ' + member.name + standard_messages["welcome to robben"]
    await member.dm_channel.send(welcome_message)
    Update_Chat(member_name= member.name,message = welcome_message)


@client.event
async def on_message(message):
    channel = await message.author.create_dm()
    if message.author.bot or message.channel.id != channel.id:
        return
    if message.author.id == 837051905057619989:
        bo2loz_message = "Bas ya 7ayawan\n3andak el HR olo bo2loz shatamni"
    global chats
    global meetings
    if "yes" in message.content.lower() or "no" in message.content.lower() :
        embed,bo2loz_message = Logic_Handling(True if "yes" in message.content.lower() else False,message.author.name,message.author.id)
    else:
        if  any(x in message.content.lower() for x in Keywords["meeting"]):
            if any(x in message.content.lower() for x in Keywords["create"]):
                bo2loz_message = message.author.name +" Do you wish to make a new meeting ?"
            elif any(x in message.content.lower() for x in Keywords["modify"]):
                bo2loz_message = message.author.name +" Do you wish to modify a meeting ?"

            elif any(x in message.content.lower() for x in Keywords["remove"]):
                bo2loz_message = message.author.name +" Do you wish to cancel a meeting ?"
            
            embed = discord.Embed(
                            description = bo2loz_message,
                            colour = discord.Colour.green()
                        )
        elif "time" in message.content.lower() and "location" in message.content.lower() and "day" in message.content.lower() and "topic" in message.content.lower():
            if "id" in message.content.lower():
                await ModifyMeeting(message)
            else:
                await MakeNewMeeting(message)
            return
        
        elif "id" in message.content.lower():
            await CancelMeeting(message)
            return
        
        elif "confirm" in message.content.lower():
            await ConfirmMeeting(message)
            return
        
        elif "excuse" in message.content.lower():
            await ExcuseMeeting(message)
            return

        else:
            bo2loz_message = "Can I help you :eyes:"
            embed = discord.Embed(
                            description = bo2loz_message,
                            colour = discord.Colour.green()
                        )
    Update_Chat(member_name= message.author.name, message= bo2loz_message)
    await message.channel.send(embed = embed)
    if message.content == "!memes":
        await SendMeme(message)


client.run(BOT_TOKEN)