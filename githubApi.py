import requests
import json
from assets import client,channels,GIT_HUB_TOKEN
from discord.ext import tasks

current_issues = []
org_name = ""
repo_name = ""

@tasks.loop(hours=1)
async def post_issues():
    global current_issues

    issue_channel = client.get_channel(channels["ISSUE CHANNEL NAME GOES HERE"])

    headers = {'Authorization': GIT_HUB_TOKEN}
    new_issues = json.loads(
        requests.get("https://api.github.com/repos/{org_name}/{repo_name}/issues?state=open", headers).content.decode())

    for issue in new_issues:
        if issue in current_issues:
            pass
        else:
            await issue_channel.send(f":beetle: :beetle: NEW ISSUE :beetle: :beetle: {issue['created_at']}\n{issue['html_url']}")
            current_issues.append(issue)
