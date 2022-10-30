import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from PyP100 import PyL530

load_dotenv('./lamp_bot/.env')
tapo_email = os.environ.get("TAPO_EMAIL")
tapo_password = os.getenv("TAPO_PASSWORD")
tapo_ip = os.getenv("LAMP_IP")
discord_token = os.getenv("DISCORD_TOKEN")
print(tapo_email)

l530 = PyL530.L530(tapo_ip, tapo_email, tapo_password)  # Creating a L530 bulb object
l530.handshake()  # Creates the cookies required for further methods
l530.login()  # Sends credentials to the plug and creates AES Key and IV for further methods

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.command()
async def luz(ctx, color: float, brightness: float):
    color_undecimal = int(color)
    brightness_undecimal = int(brightness)

    print(color_undecimal)
    print(brightness_undecimal)

    if color > 360:
        color = 360
    if brightness > 100:
        brightness = 100

    if brightness == False:
        l530.setColor(color, 100)  # Sends the set colour request
    else:
        l530.setBrightness(brightness)  # Sends the set brightness request
        l530.setColor(color, 100)  # Sends the set colour request

    await ctx.send("Light changed")


@bot.command()
async def luzoff(ctx):
    l530.turnOff()
    await ctx.send("Light off")


bot.run(discord_token)