import discord #for discord api
import requests #for api interaction
import json #for api interaction
import asyncio #for asynchronous scheduling
import random #for random delays
from datetime import datetime #for printing time
import time #basic time operations
import os #get environment variables
from dotenv import load_dotenv #load env variables

#print debug to cmd?
dodebug = False

#load env variables
load_dotenv()

#the client/bot
client = discord.Client(intents=discord.Intents.all())

#various nabends
nabends = ["nabend"]
specialnabends = ["𝔫𝔞𝔟𝔢𝔫𝔡","𝖓𝖆𝖇𝖊𝖓𝖉", "𝓷𝓪𝓫𝓮𝓷𝓭", "𝓃𝒶𝒷𝑒𝓃𝒹", "ɴᴀʙᴇɴᴅ"]

#amongusimgurl
amongusimgurl = os.getenv("AMONGUSIMGURL")

#last time jarvis said something
jarvisTime = 0

#kill loops for debug/after restart
loopkill = True
if dodebug:
    print("Killed all loops")

#returns random formatted quote
def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = "\"" + json_data[0]['q'] + "\"\n*" + json_data[0]['a'] + "*"
    return(quote)

#returns formatted lyrics
def get_lyrics(message):
    try:
        activities = message.author.activities
    except:
        return("Error: could not fetch activity")
    try:
        if activities[0] == None:
            return("Error: no activity")
    except:
        return("Error: no activity")
    final = None
    for activity in activities:
        if activity.name == "Spotify":
            final = activity
    if final == None:
        return("Error: not listening to Spotify")
    url = "https://www.google.com/search?q="
    url = url + spaceplus(final.artist) + spaceplus(final.title) + "lyrics"
    #think about implementing actual lyrics instead of url
    return(url)

#helper for url formatting (always "+" at end)
def spaceplus(input):
    split = input.split()
    res = ""
    for word in split:
        res = res + word + "+"
    return res

#helper for >looptest
async def looptest(message, interval):
    while loopkill == False:
        await message.channel.send("Looptest is running")
        await asyncio.sleep(interval)
    await message.channel.send("Looptest has been killed")

#helper for >spam
async def spam(user, message):
    try:
        dm = await user.create_dm()
        await message.channel.send("Now sending spam to " + user.display_name)
        while loopkill == False:
            await dm.send("Here, some spam for you, requested by " + message.author.name)
            await asyncio.sleep(random.randint(1, 6))
        await dm.send("Spam by " + message.author.name + " will stop now")
        await message.channel.send("Spam for " + user.display_name + " has stopped")
    except:
        await message.channel.send("Error, can't spam " + user.display_name)

#helper for >ping
async def ping(user, message):
    try:
        dm = await user.create_dm()
        await message.channel.send("Pinging " + user.display_name)
        to_delete = await dm.send(message.author.name + " pinged you")
        await to_delete.delete()
    except:
        await message.channel.send("Error, can't ping " + user.display_name)

#helper for >ping spam
async def pingspam(user, message):
    try:
        dm = await user.create_dm()
        await message.channel.send("Pinging " + user.display_name + " randomly")
        while loopkill == False:
            to_delete = await dm.send(message.author.name + " pinged you")
            await to_delete.delete()
            await asyncio.sleep(random.randint(15,180))
        await message.channel.send("Random pings for " + user.display_name + " have stopped")
    except:
        await message.channel.send("Error, can't ping " + user.display_name)

async def sendTimeSoon(channel):
    #send time after a few minutes
    await asyncio.sleep(234)
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    await channel.send(current_time)



#when bot is ready
@client.event
async def on_ready():
    if dodebug:
        print('Logged in as {0.user}'.format(client))
        print("Using discord.py version " + discord.__version__)

#when message is sent in scope of bot
@client.event
async def on_message(message):

    global jarvisTime #when used we use global variable

    #message from bot itself
    if message.author == client.user:
        return

    if message.author.bot: #don't react to other bots
        if message.author.id == os.getenv('JARVISID'): #jarvis' id
            jarvisTime = time.time()
        return

    #all commands
    if message.content.startswith(">"):

        cmd = message.content[1:]

        #list of commands
        if cmd.startswith("list"):
            await message.channel.send("Commands:" + "\n\n>test\n*tests the bot*" + "\n\n>quote\n*returns a random quote*" + "\n\n>tableflip\n*returns tableflip emote*" + "\n\n>playing <details>\n*changes the bots status to \"Playing <details>\"*" + "\n\n>watching <details>\n*changes the bots status to \"Watching <details>\"*" + "\n\n>vote <topic>\n*creates yes/no vote on <topic>*" + "\n\n>amongusimg\n*returns the glorious among us image*" + "\n\n>amongusvote\n*combines >amongusimg and >vote*" + "\n\n>latestchannel\n*returns the last text channel in which the bot was active*" + "\n\n>code\n*returns url to code for this bot*"  + "\n\n>runthrough <true/false>\n*defines if bot responds to nabend, etc*" + "\n\n>looptest <interval>\n*test a loop with interval <interval>*" + "\n\n>loopkill\n*kills all loops (e.g. spam)*"  + "\n\n>spam <?id> <mention/userid>\n*starts spamming a user defined by mention or user id*"  + "\n\n>authorize <userid>\n*authorizes a user to give commands to this bot*"  + "\n\n>deauthorize <userid>\n*deauthorizes a user to give commands to this bot*")

        #bot test
        if cmd.startswith("test"):
            await message.channel.send("Obot is running")

        #quote command
        if cmd.startswith("quote"):
            await message.channel.send(get_quote())

        #tableflip animation
        if cmd.startswith("tableflip"):
            sent = await message.channel.send("(ヽ°-°)ヽ ┬──┬")
            await asyncio.sleep(1)
            await sent.edit(content="(╯°□°)╯︵ ┻━┻")

        #set status with playing
        if cmd.startswith("playing"):
            param = cmd[8:] #after >playing and space
            await client.change_presence(status=discord.Status.online, activity=discord.Game(param))
            await message.channel.send("Bot is now playing " + param)

        #set status with watching
        if cmd.startswith("watching"):
            param = cmd[9:] #after >watching and space
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=param))
            await message.channel.send("Bot is now watching " + param)

        #set status to "Watching its own development"
        if cmd.startswith("devwatch"):
            param = "its own development"
            await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=param))
            await message.channel.send("Bot is now watching " + param)

        #requesting the among us image
        if cmd.startswith("amongusimg"):
            url = amongusimgurl
            await message.channel.send(message.author.display_name + " requested:")
            await message.channel.send(url)
            await message.delete()

        #setting up a yes/no vote
        if cmd.startswith("vote"):
            sent = await message.channel.send(message.author.display_name + " frägt: " + cmd[5:])
            await sent.add_reaction('\u2705') #green checkmark
            await sent.add_reaction('\u274C') #red cross
            await message.delete()

        #combine amongusimg and vote
        if cmd.startswith("amongusvote"):
            url = amongusimgurl
            await message.channel.send(message.author.display_name + " frägt:")
            sent = await message.channel.send(url)
            await sent.add_reaction('\u2705')
            await sent.add_reaction('\u274C')
            await message.delete()

        #returns code info
        if cmd.startswith("code"):
            await message.channel.send("This bot is running now running on a Raspberry Pi and the code isn't public anymore :(")

        #tests loops
        if cmd.startswith("looptest"):
            param = cmd[9:] #after >looptest and space
            try:
                interval = float(param)
                await message.channel.send("Looptest has started with interval " + param + "s")
                loopkill = False
                asyncio.get_event_loop().create_task(looptest(message, interval))
            except:
                await message.channel.send("Error: not a valid interval")
      

        #kills all loops
        if cmd.startswith("loopkill"):
            loopkill = True
            await message.channel.send("Killing all loopers")

        #spams a user
        if cmd.startswith("spam"):
            param = cmd[5:]
            if param.startswith("id"):
                param = cmd[8:] #after ">spam id "
                try:
                    user = await client.fetch_user(int(param))
                    if user != None:
                        loopkill = False
                        asyncio.get_event_loop().create_task(spam(user, message))
                    else:
                        await message.channel.send("Error: could not fetch that user")
                except:
                    await message.channel.send("Error: not a valid id")
            else:
                if len(message.mentions) < 1:
                    await message.channel.send("Error: you need to mention somebody")
                else:
                    loopkill = False
                    for user in message.mentions:
                        asyncio.get_event_loop().create_task(spam(user, message))

        #pings a user, then deletes the message
        if cmd.startswith("ping"):
            param = cmd[5:] #after "ping "
            if param.startswith("id"): #single ping by id
                param = cmd[8:] #after ">ping id "
                try:
                    user = await client.fetch_user(int(param))
                    if user != None:
                        loopkill = False
                        asyncio.get_event_loop().create_task(ping(user, message))
                    else:
                        await message.channel.send("Error: could not fetch that user")
                except:
                    await message.channel.send("Error: not a valid id")
            elif param.startswith("spam"): #repeated pings
                param = cmd[10:]
                if param.startswith("id"): #repeated pings by id
                    param = cmd[13:] #after ">ping spam id "
                    try:
                        user = await client.fetch_user(int(param))
                        if user != None:
                            loopkill = False
                            asyncio.get_event_loop().create_task(pingspam(user, message))
                        else:
                            await message.channel.send("Error: could not fetch that user")
                    except:
                        await message.channel.send("Error: not a valid id")
                else: #repeated pings by mention
                    if len(message.mentions) < 1:
                        await message.channel.send("Error: you need to mention somebody")
                    else:
                        loopkill = False
                        for user in message.mentions:
                            asyncio.get_event_loop().create_task(pingspam(user, message))
            else: #single ping by mention
                if len(message.mentions) < 1:
                    await message.channel.send("Error: you need to mention somebody")
                else:
                    loopkill = False
                    for user in message.mentions:
                        asyncio.get_event_loop().create_task(ping(user, message))

        if cmd.startswith("lyrics"):
            await message.channel.send(get_lyrics(message))

        if cmd.startswith("profilepic"):
            param = cmd[11:] #after ">profilepic "
            try:
                user = await client.fetch_user(int(param))
                if user != None:
                    url = str(user.avatar_url)
                    await message.channel.send(url)
                else:
                    await message.channel.send("Error: could not fetch that user")
            except:
                await message.channel.send("Error: not a valid id")
    
    #check for nabends
    if any(word in message.content.lower().replace(" ", "").replace("'", "") for word in nabends):
        await message.channel.send("nabend :)")
        #check for rip jarvis in gucci server
        if message.guild != None:
            if message.guild.id == os.getenv('GUCCIID'): #premium server gucci gucci id
                await asyncio.sleep(30)
                if time.time() - jarvisTime > 300:
                    await message.channel.send(os.getenv('JARVISIMG')) #jarvis nabend image
    
    if any(word in message.content.lower().replace(" ", "").replace("'", "") for word in specialnabends):
        sent = await message.channel.send("NABEND")
        await asyncio.sleep(1)
        for i in range(0, 5):
            await sent.edit(content="ɴABEND")
            await asyncio.sleep(1)
            await sent.edit(content="NᴀBEND")
            await asyncio.sleep(1)
            await sent.edit(content="NAʙEND")
            await asyncio.sleep(1)
            await sent.edit(content="NABᴇND")
            await asyncio.sleep(1)
            await sent.edit(content="NABEɴD")
            await asyncio.sleep(1)
            await sent.edit(content="NABENᴅ")
            await asyncio.sleep(1)
        await sent.edit(content="nabend :)")

    #check for understandable
    if "understandable" in message.content.lower():
        await message.channel.send("https://tenor.com/view/understandable-have-nice-day-have-a-great-day-have-a-good-day-nice-gif-20850110")

    #check for mood
    if "mood" in message.content.lower():
        await message.channel.send("https://i.kym-cdn.com/photos/images/facebook/001/661/247/a6e.jpg")

    #check for lol
    if "lol" in message.content.lower():
        await message.add_reaction('\N{Face with Tears of Joy}')

    #check for time (very simple)
    #if ":" in message.content.lower():
        #await sendTimeSoon(message.channel)

#when someones voice status is updated in scope of bot
@client.event
async def on_voice_state_update(member, before, after):
    connected = False
    disconnected = False
    if (before.channel == None and after.channel != None):
        connected = True
    if (before.channel != None and after.channel == None):
        disconnected = True
    if connected:
        if dodebug:
            print(str(member.name) + " connected to a voice channel")
    if disconnected:
        if dodebug:
            print(str(member.name) + " disconnected from a voice channel")

#when someones status is updated in scope of bot
@client.event
async def on_member_update(before, after):
    if before.activities != after.activities:
        if dodebug:
            print(str(after.name) + " changed their activities to " + str(after.activities))

#debug too many requests
r = requests.head(url="https://discord.com/api/v1")
try:
    if dodebug:
        print(f"Rate limit {int(r.headers['Retry-After']) / 60} minutes left")
except:
    if dodebug:
        print("No rate limit")

#run the client
client.run(os.getenv('TOKEN'))