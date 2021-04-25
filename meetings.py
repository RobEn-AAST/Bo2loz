from re import findall
from discord import Embed,Colour
from datetime import timedelta,datetime
from discord.ext import tasks
from assets import Active_meetings, client,meetings,channels,SERVER_ID,SaveConfig




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
    return today.replace(hour= hour,minute=minute).strftime("%d-%b-%Y")



@tasks.loop(hours=24)
async def remind_members():
    members = client.get_all_members()
    for x in members:
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if (datetime.strptime(y.time , '%d-%b-%Y') - datetime.today()).days + 1 < 2:
                    mem = client.get_all_members()
                    for z in mem:
                        if z.name  in y[1].not_confirmed:
                            message = "The is a meeting shceduled on " + y[1].day + "  " + y[1].time + " at" + y[1].location + "\nplease open the meetings channel and check it out\nif you cannot arrive please send me a message containing the word excuse and your excuse\n\nalways glad to help :nerd: :nerd: :nerd:"
                            channel = await z.create_dm()
                            await channel.send(message)


@tasks.loop(minutes = 1)
async def start_meetings():
    global Active_meetings
    members = (x for x in client.get_all_members())
    for x in members:
        if x.name in meetings.keys():
            for y in meetings[x.name]:
                if y != None and y.active and datetime.strptime(y.time, '%d-%b-%Y')  >= datetime.now() and not y.started:
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
                            if after.channel.id == y[1].meeting_id:
                                if member.mention in memberList:
                                    voice_channel = client.get_channel(y[1].meeting_id)
                                    users = voice_channel.members
                                    membersVC = []
                                    for user in users:
                                        if role in member.roles:
                                            membersVC.append(user.mention)
                                    memberList = list(set(memberList)^set(memids))
                                    memberList.remove(member.mention)
                                    embed = Embed(
                                        description = f"{member.mention} joined  " + y[1].topic + " meeting voice channel",
                                        colour = Colour.green()
                                    )
                                    embed.set_footer(text= f"ID: {member.id}  •  {datetime.now()}")
                                    embed.set_author(name=member.display_name, icon_url=member.avatar_url)
                                    embed.add_field(name="Missing members", value=", ".join(memberList), inline=False)
                                    embed.add_field(name="Members in the meeting", value=", ".join(membersVC))
                                    await client.get_channel(822588656627089500).send(embed=embed)


                        elif before.channel is not None and after.channel is None and role in member.roles:
                            if before.channel.id == y[1].meeting_id:
                                embed = Embed(
                                description = f"{member.mention} left " + y[1].topic + " meeting voice channel",
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
    all_members = client.get_all_members()
    for x in meetings[message.author.name]:
        if x.active == False:
            x.time = word_to_date(time,day)
            x.topic = topic
            x.active = True
            server = client.get_guild(SERVER_ID)
            categories = server.categories
            category = None
            for z in categories:
                if z.name == "Voice Channels":
                    category = z
            await server.create_voice_channel(name = topic + "Voice meeting",category = category, overwrites=None, reason = None)
            SaveConfig()
            for y in client.get_all_channels():
                if y.name == topic + " voice meeting":
                        x.meeting_id = y.id
            for y in all_members:
                if not y.bot and y.name != message.author.name :
                    x.not_confirmed.append(y.name)
                    break
            channel = client.get_channel(807682739523682330)
            await channel.send("Hello every one Bo2loz here\n" + message.author.name + " Just created a meeting!!!\n" +"meeting location : " + location + "\nmeeting time : " + day + "   " + time + "\nmeeting topic :" + topic + "\n\nif you have any excuses please send me a message containing the word (excuse) and your excuse\n\nalways glad to help :nerd: :nerd: :nerd:")
            await message.channel.send("meeting made successfully !\n your voice channel is ready !")
