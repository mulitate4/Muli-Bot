import discord
from discord.ext import commands
import json

class Listeners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		# with open("./storage/welcome-leave.json") as conf:
		# 	self.config_wl = json.load(conf)

	@commands.Cog.listener('on_member_join')
	async def welcome_and_role(self, member):
		server_joined = member.guild

		if server_joined.id == 739456173178093600:
			welcome_channel = self.bot.get_channel(739456399448342529)
			welcome_embed = discord.Embed(title="Welcome to Mulitate4's Madness!", description=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n**<@{member.id}> has entered the chat!\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**")
			welcome_embed.add_field(name="**RULES**", value="Read the rules in <#739864544989675560>", inline=True)
			welcome_embed.add_field(name="**INFO**", value=" <#743020624481353758>", inline=True)
			welcome_embed.set_thumbnail(url=member.avatar_url)
			await welcome_channel.send(embed=welcome_embed)

			initiate_role = server_joined.get_role(741962535833436170)

			await member.add_roles(initiate_role, atomic=True)

		elif server_joined.id == 729549020543975547:
			welcome_channel = self.bot.get_channel(766008524056297513)
			welcome_embed = discord.Embed(title="Welcome to Muli-bot Support Server!", description=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n**<@{member.id}> has entered the chat!\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬**")
			welcome_embed.add_field(name="**RULES**", value="Read the rules in <#766002937654673430>", inline=True)
			welcome_embed.add_field(name="**INFO**", value="Bot Info - <#729549199967911967>", inline=True)
			welcome_embed.set_thumbnail(url=member.avatar_url)
			await welcome_channel.send(embed=welcome_embed)

		# if str(server_joined.id) in self.config_wl.keys():
		# 	server_conf = self.config_wl[str(server_joined.id)]
		# 	welcome_channel_conf = int(server_conf["welcome-channel"])

		# 	welcome_channel = self.bot.get_channel(welcome_channel_conf)

		# 	title = server_conf["title"]

		# 	description = str(server_conf["sub-title"])
		# 	description.replace("{member.id}", str(member.id))

		# 	auto_role = bool(server_conf["auto-role"])
		# 	if auto_role == "True":
		# 		auto_role = True
		# 	elif auto_role == "False":
		# 		auto_role = False
		# 	else:
		# 		auto_role = False

		# 	embed = discord.Embed(title=title, description=description)
		# 	embed.set_thumbnail(url=member.avatar_url)
		# 	await welcome_channel.send(embed=embed)

		# 	if auto_role:
		# 		role_id = int(server_conf["role-id"])
		# 		role = server_joined.get_role(role_id)
		# 		await member.add_role(role, atomic=True)
			

	@commands.Cog.listener('on_member_remove')
	async def on_leave(self, member):
		server_left = member.guild

		if server_left.id == 739456173178093600:
			welcome_channel = self.bot.get_channel(739456399448342529)
			await welcome_channel.send(f"Sad to say, <@{member.id}> has left our server. :(")

		elif server_left.id == 729549020543975547:
			welcome_channel = self.bot.get_channel(766008524056297513)
			await welcome_channel.send(f"Sad to say, <@{member.id}> has left our server. :(")

def setup(bot):
	bot.add_cog(Listeners(bot))