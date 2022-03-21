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
bot.staffChannel, bot.pvpChallengesChannel, bot.currentSilphTournamentChannel = 0,0,0

#Bot Start Up
@bot.event
async def on_ready():
	#grab channels
	await grabChannelID()

#On Message Send
@bot.event
async def on_message(message):
	#verify message is not from the bot
	if message.author == bot.user:
		return
	if bot.get_channel(int(message.channel.id)) == bot.pvpChallengesChannel:
		'''
		STICKY MESSAGE FOR PVP CHALLENGES - creates a 'pinned' message at the bottom of the pvp challenges channel. Basically deletes the old message (Saved to bot.stickymessage) and
				posts a new one whenever anyone comments.
		'''
		#>>>>>>>>>>Collect current message ID
		#connect to repo
		g = Github(os.getenv("GITHUB_TOKEN"))
		repo = g.get_repo(os.getenv("GITHUB_REPO"))
		#grab contents from repo
		getStickyMessageGitHub = repo.get_contents("bot/files/PvPChallengesStickyMessageID.txt")
		#grab full content from file
		decodedStickyMessageGitHub = getStickyMessageGitHub.decoded_content.decode()
		#define vars
		stickyMessageIDs = []
		#put contents in list
		stickyMessageIDs = decodedStickyMessageGitHub.split("\n")
		#remove empty space at beginning of each string in list
		stickyMessageIDs = [item.lstrip() for item in stickyMessageIDs]
		stickyMessageIDs = list(filter(None, stickyMessageIDs))
		#>>>>>>>>>>Delete old message and post new message
		#delete previous message, otherwise alert that there is no alert to delete
		for x in stickyMessageIDs:
			try:
				messageObject = await bot.pvpChallengesChannel.fetch_message(int(x))
				await messageObject.delete()
			except:
				print('nothing to delete')
		#post new message at bottom of PvP Challenges channel
		embedVar = discord.Embed(title="Current Active Challenges:", description="**__01. It Takes Two__** *[Difficulty: Hard]*\nTo complete this challenge, you must win a battle against your opponent using 2 Pokemon (CP can be any range as long as it is eligible in the cup). The third Pokemon can be any Pokemon eligible in the cup, however it must be at 10 CP. The 10 CP Pokemon is allowed to be used in battle as well.\n\n**__02. Get Beamed__** *[Difficulty: Easy]*\nTo complete this challenge, you must successfully land a Solar Beam or Hyper Beam against an opponent and knock out the Pokemon.\n\n**__03. Overpowered__** *[Difficulty: Medium]*\nTo complete this challenge, you must win a battle against your opponent. However, all 3 Pokemon on your team must be alive (as long as it is above 0 HP) and both shields are still available (meaning unused).\n\n**__04. Community Battler__** *[Difficulty: Easy]*\nDuring community day, you must win a battle against an opponent using the Pokemon featured & its event move during the Pokemon GO Community Day.\n\n**__05. Student to Master__** *[Difficulty: Depends on Staff]*\nDefeat in a battle any BTW staff during a stream or competition.", color=0x00FF00)
		stickyMessage1 = await bot.pvpChallengesChannel.send(embed=embedVar)
		#>>>>>>>>>>Save new message ID
		stickyMessageIDs, stickyMessageIDsStr = [], ""
		stickyMessageIDs.append(str(stickyMessage1.id).lstrip())
		#add \n to each item in list to put each item on new line in file
		stickyMessageIDs = [item + "\n" for item in stickyMessageIDs]
		#transform list to string
		stickyMessageIDsStr = "".join(stickyMessageIDs)
		#update files in repo
		repo.update_file("bot/files/PvPChallengesStickyMessageID.txt", "Updated", stickyMessageIDsStr, getStickyMessageGitHub.sha)
	elif bot.get_channel(int(message.channel.id)) == bot.currentSilphTournamentChannel:
		'''
		STICKY MESSAGE FOR CURRENT SILPH TOURNAMENT - creates a 'pinned' message at the bottom of the current silph channel. Basically deletes the old message (Saved to bot.stickymessage) and
				posts a new one whenever anyone comments.
		'''
		#>>>>>>>>>>Collect current message ID
		#connect to repo
		g = Github(os.getenv("GITHUB_TOKEN"))
		repo = g.get_repo(os.getenv("GITHUB_REPO"))
		#grab contents from repo
		getStickyMessageGitHub = repo.get_contents("bot/files/SilphCupStickyMessageID.txt")
		#grab full content from file
		decodedStickyMessageGitHub = getStickyMessageGitHub.decoded_content.decode()
		#define vars
		stickyMessageIDs = []
		#put contents in list
		stickyMessageIDs = decodedStickyMessageGitHub.split("\n")
		#remove empty space at beginning of each string in list
		stickyMessageIDs = [item.lstrip() for item in stickyMessageIDs]
		stickyMessageIDs = list(filter(None, stickyMessageIDs))
		#>>>>>>>>>>Delete old message and post new message
		#delete previous message, otherwise alert that there is no alert to delete
		for x in stickyMessageIDs:
			try:
				messageObject = await bot.currentSilphTournamentChannel.fetch_message(int(x))
				await messageObject.delete()
			except:
				print('nothing to delete')
		embedVar = discord.Embed(title="B.T.W. Presents.... Nemesis Cup", description="", color=0xd45f19)
		embedVar.add_field(name="》TOURNAMENT INFORMATION",value="**Format:** Nemesis Cup\n**Link:** https://silph.gg/t/wumm/ \n**Start Time:** Apr 8th at 7pm Eastern \n**Round Time Limit:** 48hr / 2 day rounds", inline=False)
		stickyMessage1 = await bot.currentSilphTournamentChannel.send(embed=embedVar)
		#>>>>>>>>>>Save new message ID
		stickyMessageIDs, stickyMessageIDsStr = [], ""
		stickyMessageIDs.append(str(stickyMessage1.id).lstrip())
		#add \n to each item in list to put each item on new line in file
		stickyMessageIDs = [item + "\n" for item in stickyMessageIDs]
		#transform list to string
		stickyMessageIDsStr = "".join(stickyMessageIDs)
		#update files in repo
		repo.update_file("bot/files/SilphCupStickyMessageID.txt", "Updated", stickyMessageIDsStr, getStickyMessageGitHub.sha)
				
'''
CHANNEL ACCESS LIST - grab channel IDs from Heroku env list and assign it to vars
'''
async def grabChannelID():
	bot.staffChannel = bot.get_channel(int(os.getenv("STAFF_CHANNEL_ID")))
	bot.pvpChallengesChannel = bot.get_channel(int(os.getenv("PVP_CHALLENGES_CHANNEL_ID")))
	bot.currentSilphTournamentChannel = bot.get_channel(int(os.getenv("CURRENT_SILPH_TOURNAMENT_CHANNEL_ID")))
  
  
#token to run bot
bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
