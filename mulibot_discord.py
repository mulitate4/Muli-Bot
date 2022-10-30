import discord, os, asyncio, sys, traceback
from discord.ext import commands
from other_modules import api_secrets 

def get_prefix(bot, message):
	prefixes = ['>', 'give ', 'wow ']
	if not message.guild:
		return '>'
	return commands.when_mentioned_or(*prefixes)(bot, message)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
				command_prefix=get_prefix,
				description='A Bot Project by Mulitate4',
				intents = intents
				)
bot.remove_command('help')

initial_extenstions=[
				'cogs.owner',
				'cogs.listeners',
				'cogs.info',
				'cogs.music',
				'cogs.games',
				'cogs.fun',
				'cogs.moderation',
				'cogs.help',
				'cogs.utilities',
				'cogs.beta',
				'jishaku',
				]
# initial_extenstions=[
# 				'cogs.help',
# 				'cogs.owner'
# 				]


for extension in initial_extenstions:
	bot.load_extension(extension)


@bot.event
async def on_ready():
	print(str(bot.user) + " has joined discord")
	await bot.change_presence(status=discord.Status.online, activity=discord.Game("wow help for commands"))
	print(str(bot.user) + "'s status changed to custom status")

@bot.event
async def on_message(Message):
	await bot.process_commands(Message)

bot.run(api_secrets.discord_token, bot=True, reconnect=True)
