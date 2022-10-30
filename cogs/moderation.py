import discord
from discord.ext import commands
import json

class moderation(commands.Cog):
	description = "To punish that annoying person!"
	def __init__(self, bot):
		self.bot = bot
		self.update_warns()

	def update_warns(self):
		with open("./storage/warns.json") as p:
			self.warns = json.load(p)

	def save_warns(self, updated_warns: dict):
		with open('./storage/warns.json', 'w') as outfile:
			json.dump(updated_warns, outfile)

	@commands.command(name='kick', brief="kick members cause they misbehaving")
	@commands.guild_only()
	@commands.has_permissions(kick_members = True)
	async def kick(self, ctx, member: discord.Member, *, reason: str):
		await member.send("You were kicked from the server. Reason: " + reason)
		await member.kick()
		await ctx.send(f"{member} was kicked from the server, reason: {reason}")
		await ctx.message.delete()

	@commands.command(name='ban', brief='Ban members when misbehaving')
	@commands.guild_only()
	@commands.has_permissions(ban_members = True)
	async def ban(self, ctx, member: discord.Member, *, reason:str):
		await member.ban(reason=reason)
		await ctx.send(f"{member} was banned")
		await ctx.message.delete()

	@commands.command(name='unban', brief="Unban Members")
	@commands.guild_only()
	@commands.has_permissions(ban_members = True)
	async def unban(self, ctx, member_id: int):
		unban_member = discord.Object(id=member_id)
		await ctx.guild.unban(unban_member)
		await ctx.send("user has been unbanned")
		await ctx.message.delete()

	@commands.command(name='banned_members', aliases=['banned', 'bans'], brief="Gives you a list of banned members on your server")
	@commands.guild_only()
	async def banned(self, ctx):
		banned_list = []
		for member in await ctx.guild.bans():
			banned_list.append(member.user.name + "#" + str(member.user.discriminator))

		name_str = ""

		banned_embed = discord.Embed(title="Banned Members: ")
		for name in banned_list:
			name_str += f"{name}\n"

		banned_embed.add_field(name="banned: ", value=name_str, inline=False)	
		await ctx.send(embed=banned_embed)
		await ctx.message.delete()

	@commands.command(name="warn", aliases=["warning"], brief="Warn someone, if they are going against the rules")
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def warn(self, ctx, member: discord.Member=None, *, reason:str=None):
		if not member:
			await ctx.send("You must mention a user to warn using @user")
			return

		if not reason:
			await ctx.send("Enter a reason for warning. Ex) >warn @johndoe misbehaving")
			return

		self.update_warns()

		local_warns = self.warns
		server = member.guild

		str_server_id = str(server.id)
		str_member_id = str(member.id)

		if str_server_id not in local_warns.keys():
			local_warns[str_server_id] = {}
			print(local_warns[str_server_id])

		if str_member_id not in local_warns[str_server_id].keys():
			local_warns[str_server_id][str_member_id] = [reason]
		else:
			local_warns[str_server_id][str_member_id].append(reason)

		self.save_warns(local_warns)
		embed = discord.Embed(title=f"{member.name} has been warned!", description=f"Reason: {reason}")
		await ctx.send(embed=embed)

		await member.send(f"You were warned in {server.name}\nReason: {reason}")

	@commands.command(name="warns", aliases=["warnlist", "warningslist", "warnings"], brief="Check how many warns someone has on the server")
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def warnlist(self, ctx, member: discord.Member=None):
		if not member:
			await ctx.send("You must mention a user to warn using @user")
			return
		
		self.update_warns()

		local_warns = self.warns
		server = member.guild

		str_server_id = str(server.id)
		str_member_id = str(member.id)

		if str_server_id not in local_warns.keys():
			await ctx.send("That user doesn't have any warns!")
			return
		
		if str_member_id not in local_warns[str_server_id].keys():
			await ctx.send("That user doesn't have any warns!")
			return

		if len(local_warns[str_server_id][str_member_id]) == 0:
			await ctx.send("That user doesn't have any warns!")
			return

		warn_list = local_warns[str_server_id][str_member_id]
		warn_list_str = ""

		i = 1

		for warn in warn_list:
			warn_list_str += f"{str(i)}. {warn}\n"
			i += 1

		embed = discord.Embed(title=f"{member.name}'s warns:", description=warn_list_str)
		await ctx.send(embed=embed)		

	@commands.command(name="delwarn", aliases=["delwarning"], brief="Delete the warning of a user based on the number")
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def delwarn(self, ctx, member: discord.Member, warn_num:int):
		n = warn_num - 1
		# if not member:
		# 	await ctx.send("You must mention a user to warn using @user")
		# 	return
		
		self.update_warns()

		local_warns = self.warns
		server = member.guild

		str_server_id = str(server.id)
		str_member_id = str(member.id)

		if str_server_id not in local_warns.keys() or str_member_id not in local_warns[str_server_id].keys():
			await ctx.send("That user doesn't have any warns!")
			return
		
		try:
			local_warns[str_server_id][str_member_id].pop(n)
		except IndexError:
			await ctx.send("Enter a valid number")

		self.save_warns(local_warns)
		await ctx.send("Warn deleted!")

	@commands.command(name="forgive", aliases=["delallwarns"], brief="Delete all warning of a user. (Forgives them)")
	@commands.guild_only()
	@commands.has_permissions(kick_members=True)
	async def forgive(self, ctx, member: discord.Member):
		self.update_warns()

		local_warns = self.warns
		server = member.guild

		str_server_id = str(server.id)
		str_member_id = str(member.id)

		if str_server_id not in local_warns.keys() or str_member_id not in local_warns[str_server_id].keys():
			await ctx.send("That user doesn't have any warns!")
			return

		local_warns[str_server_id][str_member_id] = []
		self.save_warns(local_warns)
		embed = discord.Embed(title=f"{member.name} has been forgiven for all his sins", description="Thy has been cleansed🙏")
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(moderation(bot))