import json
import sys
from time import sleep
from views import TimetableView
try:
    import discord
    from discord import app_commands
    from dotenv import load_dotenv
    from os import environ
    from datetime import datetime
    import threading
except ImportError:
    sys.exit("""You are missing modules.
                Install them via pip install -r requirements.txt""")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
stop = False

load_dotenv()

with open('data.json', 'r') as file:
    schedule = json.load(file)


def checkTime():
    # This function runs periodically every 1 second
    thread = threading.Timer(1, checkTime)
    thread.start()
    if stop:
        thread.cancel()

    current_time = datetime.now().strftime("%H:%M:%S")

    if current_time == '08:00:00':  # check if matches with the desired time
        print('sending message')


@tree.command(name="new", guild=discord.Object(id=962644497928441916))
async def new_command(interaction: discord.Interaction, day: int, period: int, classs: str, location: str):
    """Add a new class to timetable.

    Parameters
    -----------
    day: int
        A number between 1 and 9
    period: int
        A number between 1 and 4
    classs: str
        The class in that period
    location: str
        The class location
    """
    emb = discord.Embed(title="Added a new class",
                        description=f"Set class in period {period} to {classs} in {location} on day {day}.")
    id = str(interaction.user.id)
    day = str(day)
    period = str(period)
    if not id in schedule:
        await new_user(id)
    if not str(day) in schedule[id]:
        await interaction.response.send_message(content=f"{day} (day) is not a valid 1-9 integer.")
        return
    if not str(period) in schedule[id][str(day)]:
        await interaction.response.send_message(content=f"{period} (period) is not a valid 1-4 integer.")
        return
    schedule[id][day][period]['class'] = classs
    schedule[id][day][period]['location'] = location
    await interaction.response.send_message(embed=emb, ephemeral=True)


@tree.command(name="shutdown", guild=discord.Object(id=962644497928441916))
async def shutdown_command(interaction: discord.Interaction):
    """Shutdown bot"""
    with open('data.json', 'w') as file:
        json.dump(schedule, file, indent=2)
    await interaction.response.send_message(content="Shutting down", ephemeral=True)
    sys.exit()
    sys.exit()


@tree.command(name="timetable", guild=discord.Object(id=962644497928441916))
async def timetable_command(interaction: discord.Interaction):
    """Get Timetable"""
    emb = discord.Embed(title="Timetable", description=f"Day 1")
    id = str(interaction.user.id)
    for key in schedule[id]['1'].keys():

        if schedule[id]['1'][key]['class']:
            msg = f"{schedule[id]['1'][key]['class']} in {schedule[id]['1'][key]['location']}"
        else:
            msg = "-"

        emb.add_field(name=f"Period {key}", value=msg)

    await interaction.response.send_message(embed=emb, view=TimetableView(timetable=schedule, user=id, i='1'))


@client.event
async def on_ready():
    if environ['GUILD_ID']:
        await tree.sync(guild=discord.Object(id=962644497928441916))

    print("Ready!")
    checkTime()


async def new_user(user_id):
    schedule[user_id] = {"1": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                               "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "2": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                              "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "3": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                             "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "4": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                                                                                                            "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "5": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                                                                                                                                                                                           "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "6": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                                                                                                                                                                                                                                                                          "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "7": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "8": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}, "9": {"1": {'class': "", "location": ""}, "2": {'class': "", "location": ""},
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       "3": {'class': "", "location": ""}, "4": {'class': "", "location": ""}}}
    return

client.run(environ['TOKEN'])
