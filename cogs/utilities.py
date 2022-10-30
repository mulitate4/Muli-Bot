import discord
from discord.ext import commands
import asyncio
import time

class utility(commands.Cog):
	description = "Some cool Utility commands"

	def __init__(self, bot):
		self.bot = bot
		
	@commands.command(name="bot_servers", aliases=[])
	async def server_bot(self, ctx):
		await ctx.send(f"Im currently in {len(self.bot.guilds)} servers")

	@commands.command(name="bot_users")
	async def users_bot(self, ctx):
		await ctx.send(f"Currently, {len([x.name for x in self.bot.get_all_members()])} people are using me")

	@commands.command(name="embed", brief="Sends an embed. Enter things in the format: [Mandatory] Title || [Optional] Description || [Optional] Image (Image URL), [Optional] Thumbnail (Image URL), Color (as a word). Leave empty if something isn't needed")
	async def embed(self, ctx, *, comma_seperated_values):
		title, description, image, thumbnail, color_hex = comma_seperated_values.split("||")

		colors = {
			"red": 0xe74c3c,
			"green": 0x2ecc71,
			"blue": 0x3498db,
			"teal": 0x1abc9c,
			"purple": 0x9b59b6,
			"magenta": 0xe91e63,
			"gold": 0xf1c40f,
			"orange": 0xe67e22,
			"dark": 0x36393F,
		}

		if color_hex != "" or color_hex != " ":
			color_hex = colors[color_hex.replace(" ", "")]
			color = discord.Color(color_hex)
		else:
			color = discord.Color.default()

		embed = discord.Embed(title=title, description=description, color=color)
		if image != "" or image != " ":
			embed.set_image(url=image)
		if thumbnail != "" or thumbnail != " ":
			embed.set_thumbnail(url=thumbnail)


		await ctx.send(embed=embed)

	@commands.command(name="embed_alt", brief="A different version to embed command where you can easily use \",\" without breaking the entire fucking bot")
	async def embed_alt(self, ctx, *, title=None):

		if title == None:
			await ctx.send("Usage: >`embed_alt (title)`\n`wow embed_alt (title)`")
			return("bruh no")

		def author_check(m):
			return m.channel == ctx.channel and m.author == ctx.author

		desc_ask = await ctx.send("Enter Description: ")
		description_ = await self.bot.wait_for("message", timeout=60.0, check=author_check)
		description = description_.content


		image_ask = await ctx.send("Enter Image URL. type n for no image")
		image_ = await self.bot.wait_for("message", timeout=60.0, check=author_check)
		image = image_.content


		thumbnail_ask = await ctx.send("Enter thumbnail (top right image) URL. Type n for no thumbnail")
		thumbnail_ = await self.bot.wait_for("message", timeout=60.0, check=author_check)
		thumbnail = thumbnail_.content

		colors = {
			"red": 0xe74c3c,
			"green": 0x2ecc71,
			"blue": 0x3498db,
			"teal": 0x1abc9c,
			"purple": 0x9b59b6,
			"magenta": 0xe91e63,
			"gold": 0xf1c40f,
			"orange": 0xe67e22,
			"dark": 0x36393F,
		}

		color_ask = await ctx.send(f"Enter Color name [{', '.join([color for color in colors])}]")
		color_hex_ = await self.bot.wait_for("message", timeout=60.0, check=author_check)
		color_hex = color_hex_.content.lower()

		if color_hex != "" or color_hex != " ":
			color_hex = colors[color_hex.replace(" ", "")]
			color = discord.Color(color_hex)
		else:
			color = discord.Color.default()

		embed = discord.Embed(title=title, description=description, color=color)

		if image != "n":
			embed.set_image(url=image)

		if thumbnail != "n":
			embed.set_thumbnail(url=thumbnail)

		await ctx.send(embed=embed)

		await description_.delete()
		await image_.delete()
		await thumbnail_.delete()
		await color_hex_.delete()
		await ctx.message.delete()

		await desc_ask.delete()
		await image_ask.delete()
		await thumbnail_ask.delete()
		await color_ask.delete()

	@commands.command(name="nuke", aliases=["mass_purge", "channel_purge"], brief="Nukes the channel") 
	@commands.has_permissions(manage_guild=True)       
	async def nuke(self, ctx, channel: discord.TextChannel = None):
		channel = ctx.channel if not channel else channel
		await ctx.send("Are you sure you want to delete/nuke this channel? (Yes/No)")

		def author_check(m):
			return m.channel == ctx.channel and m.author == ctx.author and m.content.lower() in ['yes', 'y', 'n', 'no']

		decision = await self.bot.wait_for("message", timeout=20.0, check=author_check)
		
		if decision.content.lower() in ['yes', 'y']:
			clone = await channel.clone()
			await channel.delete()

			await clone.send("This channel has been nuked :flushed:")

	@commands.command(name="purge", brief="Purges the given amount of messages") 
	@commands.has_permissions(manage_messages=True)      
	@commands.has_permissions(read_message_history=True)
	async def purge(self, ctx, n):
		n = int(n+1)
		try:
			await ctx.channel.purge(limit=n)
			purge_msg = await ctx.send(f"purged {n} messages!")
			await asyncio.sleep(1)
			await purge_msg.delete()
		except discord.ClientException:
			await ctx.send("Couldn't purge as messages were more than 14 days old.")
		
	@commands.command(name="av", aliases=["avatar, pfp, profile_pic"], brief="Gives you the profile picture of a user. Gives you your own, if not specified")
	async def av(self, ctx, member: discord.Member=None):
		if not member:
			member_name = ctx.author.name
			member_pfp_url = ctx.author.avatar_url
		else: 
			member_name = member.name
			member_pfp_url = member.avatar_url

		embed = discord.Embed(title=f"{member_name}'s Avatar", description=f"Requested by: {ctx.author}")
		embed.set_image(url=member_pfp_url)

		await ctx.send(embed=embed)

	@commands.command(name="ping", brief="pong")
	async def ping(self, ctx):
		start = time.perf_counter()
		message = await ctx.send("Ping...")
		end = time.perf_counter()
		duration = (end - start) * 1000
		await message.edit(content='Pong! {:.2f}ms'.format(duration))
	
def setup(bot):
	bot.add_cog(utility(bot))