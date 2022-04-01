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
bot.staffChannel, bot.pvpChallengesChannel, bot.currentSilphTournamentChannel, bot.currentSilphPracticeTournamentChannel = 0,0,0,0

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
	await message.add_reaction(":seagullllllll:959320641067159562")
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
		embedVar = discord.Embed(title="Current Active Challenges:", description="", color=0x00FF00)
		embedVar.add_field(name="March Challenges",value="[CLICK HERE TO VIEW LIST](https://discord.com/channels/811301587997687868/948750848350126080/951317452439035945)", inline=False)
		embedVar.add_field(name="April Challenges",value="Coming April 1st", inline=False)
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
		embedVar.add_field(name="》TOURNAMENT INFORMATION",value="**Format:** Nemesis Cup\n**Link:** https://silph.gg/t/wumm/ \n**Check In Code:** 4303\n**Start Time:** Apr 8th at 7pm Eastern\n**Round Time Limit:** 48hr / 2 day rounds", inline=False)
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
	elif bot.get_channel(int(message.channel.id)) == bot.currentSilphPracticeTournamentChannel:
		#>>>>>>>>>>Collect current message ID
		#connect to repo
		g = Github(os.getenv("GITHUB_TOKEN"))
		repo = g.get_repo(os.getenv("GITHUB_REPO"))
		#grab contents from repo
		getStickyMessageGitHub = repo.get_contents("bot/files/PracticeSilphCupStickyMessageID.txt")
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
				messageObject = await bot.currentSilphPracticeTournamentChannel.fetch_message(int(x))
				await messageObject.delete()
			except:
				print('nothing to delete')
		embedVar = discord.Embed(title="B.T.W. Presents.... TBA", description="", color=0x367900)
		embedVar.add_field(name="》TOURNAMENT INFORMATION",value="**Format:** TBA Cup\n**Link:** TBA \n**Check In Code:** TBA\n**Start Time:** Apr 22nd at 7pm Eastern\n**Round Time Limit:** 48hr / 2 day rounds", inline=False)
		stickyMessage1 = await bot.currentSilphPracticeTournamentChannel.send(embed=embedVar)
		#>>>>>>>>>>Save new message ID
		stickyMessageIDs, stickyMessageIDsStr = [], ""
		stickyMessageIDs.append(str(stickyMessage1.id).lstrip())
		#add \n to each item in list to put each item on new line in file
		stickyMessageIDs = [item + "\n" for item in stickyMessageIDs]
		#transform list to string
		stickyMessageIDsStr = "".join(stickyMessageIDs)
		#update files in repo
		repo.update_file("bot/files/PracticeSilphCupStickyMessageID.txt", "Updated", stickyMessageIDsStr, getStickyMessageGitHub.sha)		
'''
CHANNEL ACCESS LIST - grab channel IDs from Heroku env list and assign it to vars
'''
async def grabChannelID():
	bot.staffChannel = bot.get_channel(int(os.getenv("STAFF_CHANNEL_ID")))
	bot.pvpChallengesChannel = bot.get_channel(int(os.getenv("PVP_CHALLENGES_CHANNEL_ID")))
	bot.currentSilphTournamentChannel = bot.get_channel(int(os.getenv("CURRENT_SILPH_TOURNAMENT_CHANNEL_ID")))
	bot.currentSilphPracticeTournamentChannel = bot.get_channel(int(os.getenv("CURRENT_PRACTICE_SILPH_TOURNAMENT_CHANNEL_ID")))
  
  
#token to run bot
bot.run(os.getenv("DISCORD_TOKEN"), reconnect=True)
