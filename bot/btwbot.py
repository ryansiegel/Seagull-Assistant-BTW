import discord,asyncio,os,requests,string
from datetime import datetime, timedelta, date
from discord.ext import commands, tasks
from discord.ui import Button, View
from github import Github

#discord bot setup and log in
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', description="This is a Helper Bot", intents=intents)

@bot.event
async def on_ready():
  print('ready')
  
  
#token to run bot
bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
