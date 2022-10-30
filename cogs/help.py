import discord
from discord.ext import commands

class MyHelpCommand(commands.MinimalHelpCommand):

	async def send_bot_help(self, mapping):
		ctx = self.context
		bot = ctx.bot
		cogs = bot.cogs

		cog_list_str = "```\n"
		for cog in cogs:
			if cog not in ["OwnerCog", "Listeners", "Jishaku", "helpcog", "Beta"]:
				cog_list_str += f"{cog}\n"
		cog_list_str += "```"

		help_embed = discord.Embed(title='MuliBot Help Commands', description='Prefixes = `>, give , wow )', color = discord.Color.purple())
		
		help_embed.add_field(name='ℹ **Help!**', value=f'`{self.clean_prefix}help <command>/<category>` for more help on a command!', inline=False)

		help_embed.add_field(name="**Categories**:", value=cog_list_str, inline=False)

		help_embed.add_field(name="**Example**:", value=f'''
			`{self.clean_prefix}help fun`\n
			`{self.clean_prefix}help hello`
		''', inline=False)

		help_embed.add_field(name="**Found a bug?** 🐞", value='''
			Join the Muli-bot support server, and let the creator know :)\n
			Join server - [here](https://discord.gg/bWqcFBU3r7)
		''')

		help_embed.set_thumbnail(url = bot.user.avatar_url)
		help_embed.set_footer(text='Bot Dev: MUwUlitate4#9118')
		help_embed = await ctx.send(embed=help_embed)

	def get_command_aliases(self, command):
		if not command.aliases:
			return 'No aliases for this command'
		else:
			return f'command aliases are [`{"` | `".join([alias for alias in command.aliases])}`]'

	def get_command_description(self, command):
		if not command.short_doc:
			return 'No Information for this command for now :flushed:'
		else:
			return command.short_doc

	async def send_command_help(self, command):
		ctx = self.context
		bot = ctx.bot
		
		embed = discord.Embed(name=f"Command Help - {command.name}", colour=discord.Color.purple(), timestamp=ctx.message.created_at)
		embed.set_author(name=f"Help - {command.name}")
		embed.set_thumbnail(url=f"{bot.user.avatar_url}")
		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{bot.user.avatar_url}")
		embed.add_field(name="**Command**", value=f"`{command.name}`", inline=True)
		embed.add_field(name="**Usage**", value=f"`{self.clean_prefix}{command.name}`", inline=True)
		embed.add_field(name="**Description**", value=f"**`{self.get_command_description(command)}`**", inline=False)
		embed.add_field(name="**Aliases**", value=f"{self.get_command_aliases(command)}", inline=False)
		
		embed.add_field(name="**Quick Tip**", value="*Invite Me : `>invite`*", inline=False)
		await ctx.send(embed=embed)

	async def send_cog_help(self, cog):
		if cog.qualified_name in ["OwnerCog", "Listeners", "Jishaku", "helpcog", "Beta"]:
			return 

		ctx = self.context
		bot = ctx.bot
		commands_str = ""
		for command in cog.get_commands():
			print
			signature = " ".join(self.get_command_signature(command).split(" ")[2:])
			if signature == "":
				commands_str += f"`{command.name}` - {self.get_command_description(command)}\n"
			else:
				commands_str += f"`{command.name} {signature}` - {self.get_command_description(command)}\n"

		cog_desc = "No description for now!"
		if cog.description:
			cog_desc = cog.description

		embed = discord.Embed(title=f"Category Help - {cog.qualified_name}", description=cog_desc, colour=discord.Color.purple(), timestamp=ctx.message.created_at)
		embed.add_field(name="**Commands**", value=commands_str)
		embed.set_footer(text=f"Requested by {ctx.author}", icon_url=f"{ctx.author.avatar_url}")
		embed.add_field(name="**Hot Tip**", value="*Invite Me : `>invite`*", inline=False)
		await ctx.send(embed=embed)
	
class helpcog(commands.Cog):
	def __init__(self, bot):
		self._original_help_command = bot.help_command
		bot.help_command = MyHelpCommand()
		bot.help_command.cog = self

	def cog_unload(self):
		self.bot.help_command = self._original_help_command

def setup(bot):
	bot.add_cog(helpcog(bot))