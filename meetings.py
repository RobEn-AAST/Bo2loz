from asyncio.windows_events import NULL
from re import findall
from discord import Embed,Colour
from datetime import timedelta,datetime
from discord.ext import tasks
from assets import Active_meetings, client,meetings,SERVER_ID,SaveConfig

def word_to_date(Time,day):
    day = day.replace(" ", "")
    time = findall("[0-9][0-2]*:[0-9]{2}",Time)[0]
    state = findall("[p|a|P|A]",Time)[0]
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



@tasks.loop(hours=24)
async def remind_members():
    members = client.get_all_members()
    for x in members:
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if (y.time - datetime.today()).days + 1 < 2:
                    for z in client.get_all_members():
                        if not z.bot and z.name not in y.confirmed:
                            message = "You did not confirm on the meeting shceduled on " + y.time.strftime("%c") + " at " + y.location + "Please check it out in the meetings channel\n\nalways glad to help :nerd: :nerd: :nerd:"
                            channel = await z.create_dm()
                            await channel.send(message)


@tasks.loop(minutes = 1)
async def start_meetings():
    global Active_meetings
    members = (x for x in client.get_all_members())
    for x in members:
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if y != None and y.active and  y.time < datetime.now() and not y.started:
                    y.started = True
                    Active_meetings.append(x.id)
                    channel = client.get_channel(807682739523682330)
                    await channel.send("Hello every one...Bo2loz here,\nThe " + y.topic + " meeting will start now so please enter the voice channel now.\nGood luck Team !!!")


@client.event
async def on_voice_state_update(member, before, after):
    role = member.guild.get_role(822598861402013707)
    guild = client.get_guild(SERVER_ID)
    memberList = []
    for user in guild.members:
        if role in user.roles:
            memberList.append(user.mention)

    for x in Active_meetings:
        voice_channel = client.get_channel(x)

        members = voice_channel.members

        membersVC = []
        for member in members:
            if role in member.roles:
                membersVC.append(member.mention)
        for x in client.get_all_members():
            if x.name in meetings.keys():
                for y in meetings[x.name]:
                    if y.active == True:
                        if before.channel is None and after.channel is not None and role in member.roles:
                            if after.channel.id == y.meeting_id:
                                if member.mention in memberList:
                                    voice_channel = client.get_channel(y.meeting_id)
                                    users = voice_channel.members
                                    membersVC = []
                                    for user in users:
                                        if role in member.roles:
                                            membersVC.append(user.mention)
                                    memberList = list(set(memberList)^set(memids))
                                    memberList.remove(member.mention)
                                    embed = Embed(
                                        description = f"{member.mention} joined  " + y.topic + " meeting voice channel",
                                        colour = Colour.green()
                                    )
                                    embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
                                    embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                                    embed.add_field(name="Missing members", value=", ".join(memberList), inline=False)
                                    embed.add_field(name="Members in the meeting", value=", ".join(membersVC))
                                    await client.get_channel(822588656627089500).send(embed=embed)


                        elif before.channel is not None and after.channel is None and role in member.roles:
                            if before.channel.id == y.meeting_id:
                                embed = Embed(
                                description = f"{member.mention} left " + y.topic + " meeting voice channel",
                                colour = Colour.red()
                                )
                                embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
                                embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                                await client.get_channel(822588656627089500).send(embed=embed)

async def MakeNewMeeting(message):
    time = findall("[Tt]ime\s*:\s*[0-9][0-2]*:[0-9]{2}\s*[A|a|P|p][m|M],*",message.content.lower())[0]
    day = findall("[Dd]ay\s*:\s*\w+day\s*,*",message.content.lower())[0]
    location = findall("[Ll]ocation\s*:.+,*",message.content.lower())[0]
    topic = findall("[Tt]opic\s*:.+,*",message.content.lower())[0]
    time = time[time.index(':') + 1:time.index(',') if ',' in time else len(time)].strip()
    day = day[day.index(':') + 1:day.index(',')  if ',' in day else len(day)].strip()
    location = location[location.index(':') + 1:location.index(',') if ',' in location else len(location)].strip()
    topic = topic[topic.index(':') + 1:topic.index(',') if ',' in topic else len(topic)].strip()
    for x in meetings[message.author.name]:
        if x.active == False:
            x.time = word_to_date(time,day)
            x.topic = topic
            x.active = True
            x.location = location
            x.confirmed.append(message.author.name)
            server = client.get_guild(SERVER_ID)
            categories = server.categories
            category = None
            for z in categories:
                if z.name == "Voice Channels":
                    category = z
            await server.create_voice_channel(name = topic + " Voice meeting",category = category, overwrites=None, reason = None)
            for y in client.get_all_channels():
                if y.name == topic + " Voice meeting":
                        x.meeting_id = y.id
            meetingid = str(x.meeting_id)
            SaveConfig()
            channel = client.get_channel(807682739523682330)
            await channel.send('Hello every one Bo2loz here\n' + message.author.name + ' Just created a meeting!!!\nmeeting location : ' + location + '\nmeeting time : ' + x.time.strftime("%c") + '\nmeeting topic :' + topic + '\nmeeting id : ' + meetingid + '\n\nif you have any excuses please send me a message containing the word excuse + meeting id + your excuse (example : excuse 123456789 I was sick)\nTo confirm send me a message containing the word confirm + meeting id (example : confirm 123456789)\n\nalways glad to help :nerd: :nerd: :nerd:')
            await message.channel.send("meeting made successfully !\n your voice channel is ready !\n meeting id : " + meetingid)


async def ModifyMeeting(message):
    time = findall("[Tt]ime\s*:\s*[0-9][0-2]*:[0-9]{2}\s*[A|a|P|p][m|M],*",message.content.lower())[0]
    day = findall("[Dd]ay\s*:\s*\w+day\s*,*",message.content.lower())[0]
    location = findall("[Ll]ocation\s*:.+,*",message.content.lower())[0]
    topic = findall("[Tt]opic\s*:.+,*",message.content.lower())[0]
    id = findall("[iI][Dd]\s*:.+,*",message.content.lower())[0]
    time = time[time.index(':') + 1:time.index(',') if ',' in time else len(time)].strip()
    day = day[day.index(':') + 1:day.index(',')  if ',' in day else len(day)].strip()
    location = location[location.index(':') + 1:location.index(',') if ',' in location else len(location)].strip()
    topic = topic[topic.index(':') + 1:topic.index(',') if ',' in topic else len(topic)].strip()
    id = id[id.index(':') + 1:id.index(',') if ',' in id else len(id)].strip()
    current = NULL
    for x in meetings[message.author.name]:
        if x.active == True and x.id == id:
            x.time = word_to_date(time,day)
            x.topic = topic
            x.location = location
            current = x
            break
    channel = client.get_channel(807682739523682330)
    await channel.send("Hello every one Bo2loz here\n" + message.author.name + " Just modified the "+ current.topic +" meeting!!!\n" +"meeting location : " + location + "\nmeeting time : " + day + "   " + time + "\nmeeting topic :" + topic + "\n\nif you have any excuses please send me a message containing the word (excuse) and your excuse\n\nalways glad to help :nerd: :nerd: :nerd:")
    await message.channel.send("meeting modified successfully !")


async def CancelMeeting(message):
    id = findall("[iI][Dd]\s*:.+,*",message.content.lower())[0]
    id = id[id.index(':') + 1:len(id)].strip()
    for x in meetings[message.author.name]:
        if x.active == True and x.id == id:
            meetings[message.author.name].remove(x)
            channel = client.get_channel(id)
            await channel.delete()
            channel = client.get_channel(807682739523682330)
            await channel.send("Hello every one Bo2loz here\n" + message.author.name + " Just Cancelled the "+ x.topic + " meeting\n\nalways glad to help :nerd: :nerd: :nerd:")
            await message.channel.send("meeting Cancelled successfully !")
            return
    await message.channel.send("Error cancelling the meeting\n please check your meeting id")
    return


async def ConfirmMeeting(message):
    id = int(findall(r'[0-9]+', message.content.lower())[0])
    for x in meetings:
        for y in meetings[x]:
            if y.active == True and y.meeting_id == id and message.author.name not in y.confirmed:
                for z in client.get_all_members():
                    if z.id == y.admin:
                        channel = await z.create_dm()
                        y.confirmed.append(message.author.name)
                        if message.author.name in y.excuse.keys():
                            y.excuse.pop(message.author.name , None)
                        await channel.send(message.author.name + "has confirmed the " + y.topic + " meeting")
                        await message.channel.send("Confirmation Successfull")
                        SaveConfig()
                        return
    return


async def ExcuseMeeting(message):
    id = findall(r'[0-9]+', message.content.lower())[0]
    excuse = findall("[Ee][Xx][cC][Uu][Ss][Ee]\s*:.+", message.content.lower())[0]
    excuse = excuse[excuse.index(':') + 1:len(excuse)].strip()
    excuse = ''.join([i for i in excuse if not i.isdigit()])
    for x in meetings:
        for y in meetings[x]:
            if y.active == True and y.meeting_id == int(id) :
                for z in client.get_all_members():
                    if z.id == y.admin:
                        channel = await z.create_dm()
                        y.excuse[message.author.name] = excuse
                        if message.author.name in y.confirmed:
                            y.confirmed.remove(message.author.name)
                        await channel.send(message.author.name + " said he cannot attend the " + y.topic + " meeting\nexcuse : " + excuse)
                        await message.channel.send("Your excuse has been submitted to the meeting host\nSorry to hear that :sob:")
                        SaveConfig()
                        return
    return

