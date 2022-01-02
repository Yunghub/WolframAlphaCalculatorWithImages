##########################################################################
#                          Discord Maths Bot                             #
#       This is a calculator Discord bot that uses Wolfram Alpha         #
#           You can use this to solve and display equations              #
#                                                                        #
#                     This is coded by Yung#1000                         #
#                                                                        #
#                   Copyright (c) 2021, YungCZ.com                       #
#                       All rights reserved.                             #
#  This source code is licensed under the BSD-style license found in the #
#       LICENSE file in the root directory of this source tree.          #
#           This software is under the Apache-2.0 License                #
##########################################################################

# Version 1.1.1 Bug Fix

# Importing Libraries
import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import requests
import datetime
import io
import json
from urllib import parse as urlparse

# Setting Variables
global config
config = None

# Creating config.yml if not existance
def start():
    global config
    try:
        with open("config.json", "r") as c:
            config = json.load(c)
    except FileNotFoundError:
        print ("Config not found, making one")
        with open("config.json","w") as c:
            json.dump({'WolframAlplha_API_TOKEN': 'TOKEN', 
            'Discord_TOKEN': 'TOKEN',
            'Activity': 'Bot activity here',
            'Prefix': 'y, maths',
            'Embed_Title': 'Yungs Math Bot',
            'Embed_Title_URL': 'https://yungcz.com',
            'Embed_Description': 'I like to solve maths equations, just like Kamran the mathematician!',
            'Embed_Colour': 0xFFFFFF,
            'Embed_Thumbnail': 'https://i.imgur.com/U067iC8.jpg'
            }, c, indent=2)
        raise Exception ("Fill in your config.json before continuing")
        exit()

# Perform start function
start()

# Register the bot
bot = commands.Bot(command_prefix=config["Prefix"])
bot.remove_command("help")

# On command help
@bot.command()
async def help(ctx):
    embed = discord.Embed(title = config["Embed_Title"], url = config["Embed_Title_URL"], colour = config["Embed_Colour"], description = config["Embed_Description"], timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url = config["Embed_Thumbnail"])
    embed.add_field(name="⭐ Prefix", value = config["Prefix"], inline=False)
    embed.add_field(name="❓ How to use", value = "Type %s followed by maths! \nBe aware WolframAlphas API is quite slow, its doing a lot of complicated mathematics, please be patient and the answer will come to you." % config["Prefix"], inline=False)
    embed.add_field(name="🤖 Info", value = "This bot is completely open source [Here](https://github.com/Yunghub/WolframAlphaCalculatorWithImages)", inline=True)
    embed.add_field(name="🔗 Invite", value = "I want you in my server! [here](https://yungcz.com/yungbot)", inline=True)
    embed.set_footer(text = "This bot is coded by Yung, open source at Github, YungHub, YungCZ.com", icon_url="https://i.imgur.com/U067iC8.jpg")
    await ctx.send(embed = embed)
    return

@bot.event
async def on_ready():
    try:
        activity = config["Activity"]
        await bot.change_presence(activity=discord.Streaming(name=activity, url="http://www.twitch.tv/ninja"))
        print("Started!")
    except:
        print ("Something is wrong with starting the bot, are you sure everything you've entered is correct?")
        raise Exception

# Ignore command not found, no more console spam
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

# Listens for maths
@bot.listen()
async def on_message(message): # Ignores the help command
    prefix = config["Prefix"]
    if prefix + "help" in message.content.lower():
        return
    elif prefix in message.content.lower(): # When it is not the maths command
        await message.add_reaction("⌛")
        ask = message.content # Store what the user has asked
        
        # Ignores the prefix
        ask = ask[len(config["Prefix"]):]
        # Format API URL
        url = str("http://api.wolframalpha.com/v1/simple?appid=" + str(config['WolframAlplha_API_TOKEN']) + "&i=" + urlparse.quote(ask))

        # Get request
        request = requests.get(url)

        # Check for invalid appid returned from API
        if request.content == "Error 1: Invalid appid":
            await message.channel.send("Invalid App ID")
        else:
            # Converts the media from WolframAlpha API to be sent on discord
            await message.channel.send(file=discord.File(fp=io.BytesIO(request.content), filename="WolframAlphaBot.gif"))
            await message.clear_reaction("⌛")
            await message.add_reaction("✅")
        return


bot.run(config["Discord_TOKEN"])
