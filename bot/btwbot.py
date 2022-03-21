import discord,asyncio,os,requests,string
from datetime import datetime, timedelta, date
from discord.ext import commands, tasks
from discord.ui import Button, View
from github import Github

#discord bot setup and log in
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', description="This is a Helper Bot", intents=intents)

'''
CHANNEL ACCESS LIST
'''
#save IDs of channels
bot.staffChannel, bot.pvpChallengesChannel = 0,0

'''
STICKY MESSAGE
'''
#save current sticky message to string to delete when new message is posted
bot.stickyMessagePvPChallenges = ""

'''
BOT START UP
'''
@bot.event
async def on_ready():
	#grab channels
	await grabChannelID()
	await bot.staffChannel.send('Hey there fuckers. It\'s me, your bot. I am online and ready to fuck shit up!')

@bot.event
async def on_message(message):
	if bot.get_channel(int(message.channel.id)) == bot.pvpChallengesChannel:
		#verify message is not from the bot
		if message.author == bot.user:
			return
		'''
		STICKY MESSAGE - creates a 'pinned' message at the bottom of the intro channel. Basically deletes the old message (Saved to bot.stickymessage) and
				posts a new one whenever anyone comments.
		'''
		#delete previous message, otherwise alert that there is no alert to delete
		try:
			await bot.stickyMessagePvPChallenges.delete()
		except:
			print('nothing to delete')
		#post new message at bottom of intro channel
		embedVar = discord.Embed(title="TEST", description="To complete any of the challenges below, the following must also be followed:\n01. All challenges can only be earned after reaching rank 15 in GBL (you must be rank 15 or above when this is earned), or completed in a ranked Silph competition, or an unranked tournament host by BTW.\n02. If it is clear that opponent is trying to tank their ranking and not actually playing the match to win, that battle can not be counted.\n03. Only battles in GBL, Silph, or any other competitive play can be counted.", color=0xe1c2f2)
		embedVar.add_field(name="Current Active Challenges:",value="**__01. It Takes Two__** *[Difficulty: Hard]*\nTo complete this challenge, you must win a battle against your opponent using 2 Pokemon (CP can be any range as long as it is eligible in the cup). The third Pokemon can be any Pokemon eligible in the cup, however it must be at 10 CP. The 10 CP Pokemon is allowed to be used in battle as well.\n\n**__02. Get Beamed__** *[Difficulty: Easy]*\nTo complete this challenge, you must successfully land a Solar Beam or Hyper Beam against an opponent and knock out the Pokemon.\n\n**__03. Overpowered__** *[Difficulty: Medium]*\nTo complete this challenge, you must win a battle against your opponent. However, all 3 Pokemon on your team must be alive (as long as it is above 0 HP) and both shields are still available (meaning unused).\n\n**__04. Community Battler__** *[Difficulty: Easy]*\nDuring community day, you must win a battle against an opponent using the Pokemon featured & its event move during the Pokemon GO Community Day.\n\n**__05. Student to Master__** *[Difficulty: Depends on Staff]*\nDefeat in a battle any BTW staff during a stream or competition.", inline=False)
		bot.stickyMessagePvPChallenges = await bot.pvpChallengesChannel.send(embed=embedVar)
	
	
	
	
'''
CHANNEL ACCESS LIST - grab channel IDs from Heroku env list and assign it to vars
'''
async def grabChannelID():
	bot.staffChannel = bot.get_channel(int(os.getenv("STAFF_CHANNEL_ID")))
	bot.pvpChallengesChannel = bot.get_channel(int(os.getenv("PVP_CHALLENGES_CHANNEL_ID")))
  
  
#token to run bot
bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
