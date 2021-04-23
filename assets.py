import json
from discord import Intents,Client
from praw import Reddit
import re
from datetime import timedelta,datetime
from discord.ext import tasks
from collections import namedtuple
intents = Intents.default()
intents.members = True
client  = Client(intents = intents)



Active_meetings = []


class meeting :
    def __init__(self, input):
        if type(input) == str:
            self.admin = input
            self.time = None
            self.location = None
            self.topic= None
            self.active = False
            self.not_confirmed = []
            self.meeting_id = None
            self.meeting_attendance = []
            self.started = False
        else:
            self.admin = input["admin"]
            self.time = input["time"]
            self.location = input["location"]
            self.topic= input["topic"]
            self.active = input["admin"]
            self.not_confirmed = input["not_confirmed"]
            self.meeting_id = input["meeting_id"]
            self.meeting_attendance = input["meeting_attendance"]
            self.started = input["started"]
        return
    @staticmethod
    def dic(ob):
        dictionary = {
            "admin" : ob.admin,
            "time" : ob.time,
            "location" : ob.location,
            "topic" : ob.topic,
            "admin" : ob.admin,
            "not_confirmed" : ob.not_confirmed,
            "meeting_id" : ob.meeting_id,
            "meeting_attendance" : ob.meeting_attendance,
            "started" : ob.started
        }
        return dictionary


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
    meetings_map = {}
    for x in meetings.keys():
        if x not in meetings_map:
            meetings_map[x] = []
        for y in meetings[x]:
            y.admin = x
            meetings_map[x].append(meeting.dic(y))
    json_string = {
        "BOT-TOKEN" : BOT_TOKEN,

        "GitHub-Token" : GIT_HUB_TOKEN,

        "Server-ID" : str(SERVER_ID),

        "chats" : chats,

        "meetings" : meetings_map,

        "colors" : list(map(str,list(map(hex,colors)))),

        "Keywords" : Keywords,

        "reddit" : {
            "client_id" : reddit_config["client_id"],
            "client_secret" : reddit_config["client_secret"],
            "username" : reddit_config["username"],
            "password" : reddit_config["password"],
            "user_agent" : reddit_config["user_agent"]
        },
        "last-save" : datetime.now().strftime("%d-%b-%Y %H:%M:%S"),
        "synchronization-interval" : sync_interval
    }
    with open('settings.json', 'w', encoding='utf-8') as f:
        json.dump(json_string, f, ensure_ascii=False, indent=4)


@tasks.loop(hours = 1)
async def update_config():
    SaveConfig()

with open('settings.json', 'r', encoding='utf-8') as f:
    configration = json.load(f)
BOT_TOKEN = configration["BOT-TOKEN"]
GIT_HUB_TOKEN = configration["GitHub-Token"]
SERVER_ID = int(configration["Server-ID"])
y = configration["meetings"]
meetings = {}
for x in y.keys():
    if x not in  meetings.keys():
        meetings[x] = []
    for z in y[x]:
        meetings[x].append(meeting(z))
colors = list(map(lambda x: int(x, 16),configration["colors"]))
chats = configration["chats"]
Keywords = configration["Keywords"]
reddit_config = configration["reddit"]
reddit = Reddit(
    client_id= reddit_config["client_id"],
    client_secret= reddit_config["client_secret"],
    username =  reddit_config["username"],
    password =  reddit_config["password"],
    user_agent= reddit_config["user_agent"],
    check_for_async=False
    )
Last_SaveConfig_time = datetime.strptime(configration["last-save"], '%d-%b-%Y %H:%M:%S')
sync_interval = configration["synchronization-interval"]

channels = {
    "Text" : {},
    "Audio" : {}
}
