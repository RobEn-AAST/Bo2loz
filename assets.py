import json
from discord import Intents,Client
from praw import Reddit
import re
from datetime import timedelta,datetime
from discord.ext import tasks

intents = Intents.default()
intents.members = True
client  = Client(intents = intents)


standard_messages = {
    "new meeting info" : ''' please give me the meeting information in one message separated by commas...meeting information are
1 - meeting day
2 - meeting time >> ex: (2:30 pm)
3 - meeting location
4 - meeting topic

example >> day : wednesday,time : 3:40 pm,location : nasr city, topic : 2a3da ray2a

''',
    "welcome to robben" : ''' , welcome to Robben AI team !!!\nRules :
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
}

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

def SaveConfig():
    json_string = {
        "BOT-TOKEN" : TOKEN,

        "chats" : chats,

        "meetings" : meetings,

        "colors" : colors,

        "Keywords" : Keywords,

        "reddit" : {
            "client_id" : reddit_config["client ID"],
            "client_secret" : reddit_config["client secret"],
            "username" : reddit_config["reddit username"],
            "password" : reddit_config["reddit password"],
            "user_agent" : reddit_config["user agent"]
        },
        "last-SaveConfig" : datetime.now(),
        "synchronization-interval" : sync_interval
    }
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(json_string, f, ensure_ascii=False, indent=4)


@tasks.loop(hours = 1)
async def update_config():
    SaveConfig()

with open('settings.json', 'r', encoding='utf-8') as f:
    configration = json.load(f)
TOKEN = configration["BOT-TOKEN"]
meetings = configration["meetings"]
colors = configration["colors"]
chats = configration["chats"]
Keywords = configration["Keywords"]
reddit_config = configration["reddit"]
reddit = Reddit(
    client_id= reddit_config["client ID"],
    client_secret= reddit_config["client secret"],
    username =  reddit_config["reddit username"],
    password =  reddit_config["reddit password"],
    user_agent= reddit_config["user agent"],
    check_for_async=False
    )
Last_SaveConfig_time = configration["last-SaveConfig"]
sync_interval = configration["synchronization-interval"]

channels = {
    "Text" : {},
    "Audio" : {}
}
