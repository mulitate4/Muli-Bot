import discord
from discord.ext import commands
import praw
import requests
import random
from other_modules import api_secrets

reddit_client = praw.Reddit(
				client_id=api_secrets.reddit_client_id,
				client_secret=api_secrets.reddit_client_secret,
				password=api_secrets.reddit_password,
				user_agent=api_secrets.reddit_user_agent,
				username=api_secrets.reddit_username
				)

class fun(commands.Cog):
	description = "Fun stuff like memes, coin toss, and more!"

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='hello', aliases=['hi', 'sup'], brief="Hello!")
	async def hello(self, ctx):
		await ctx.send(f"Hello {ctx.author.mention}")

	def random_coin_toss(self):
		return random.choice(['Heads', 'Tails'])

	def reddit_memes(self):
		while True:
			req = reddit_client.subreddit("memes").random()
			if "jpg" in req.url or "png" in req.url:
				meme_embed = discord.Embed(title="Heres Your Meme Man")
				meme_embed.set_image(url=req.url)
				return meme_embed
			else:
				continue

	@commands.command(name="memes", aliases=['meme'], brief="Gives you a random meme from r/memes")
	async def memes(self, ctx):
		await ctx.send(embed = self.reddit_memes())

	@commands.command(name="coin_toss", aliases=["toss", "coin"], brief="Can't decide? Use coin toss!")
	async def coin_toss(self, ctx):
		await ctx.send(embed=discord.Embed(title=self.random_coin_toss()))

	@commands.command(name='say', brief='Make the bot say something, and delete your command message')
	async def say(self, ctx, *, input: str):
		await ctx.send(input)
		await ctx.message.delete()

	@commands.command(name="freevbucks", brief="Get freevbucks here!")
	async def freevbucks(self, ctx):
		await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
		await ctx.send("Get RICKROLLED Kid")

def setup(bot):
	bot.add_cog(fun(bot))
import discord
from discord.ext import commands
import praw
import requests
import random
from other_modules import api_secrets

reddit_client = praw.Reddit(
	client_id=api_secrets.reddit_client_id,
	client_secret=api_secrets.reddit_client_secret,
	password=api_secrets.reddit_password,
	user_agent=api_secrets.reddit_user_agent,
	username=api_secrets.reddit_username
)

class fun(commands.Cog):
	description = "Fun stuff like memes, coin toss, and more!"

	def __init__(self, bot):
		self.bot = bot

	@commands.command(name='hello', aliases=['hi', 'sup'], brief="Hello!")
	async def hello(self, ctx):
		await ctx.send(f"Hello {ctx.author.mention}")

	def random_coin_toss(self):
		return random.choice(['Heads', 'Tails'])

	def reddit_memes(self):
		while True:
			req = reddit_client.subreddit("memes").random()
			if "jpg" in req.url or "png" in req.url:
				meme_embed = discord.Embed(title="Heres Your Meme Man")
				meme_embed.set_image(url=req.url)
				return meme_embed
			continue

	@commands.command(name="memes", aliases=['meme'], brief="Gives you a random meme from r/memes")
	async def memes(self, ctx):
		await ctx.send(embed = self.reddit_memes())

	@commands.command(name="coin_toss", aliases=["toss", "coin"], brief="Can't decide? Use coin toss!")
	async def coin_toss(self, ctx):
		await ctx.send(embed=discord.Embed(title=self.random_coin_toss()))

	@commands.command(name='say', brief='Make the bot say something, and delete your command message')
	async def say(self, ctx, *, input: str):
		await ctx.send(input)
		await ctx.message.delete()

	@commands.command(name="freevbucks", brief="Get freevbucks here!")
	async def freevbucks(self, ctx):
		await ctx.send("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
		await ctx.send("Get RICKROLLED Kid")

	@commands.command(name="bored", aliases=["imbored", "bore"], brief="Things to do when you're bored!")
	async def bored(self, ctx):
		resp = requests.get("https://www.boredapi.com/api/activity").json()
		activity = resp['activity']
		type_ = resp['type']
		link = resp['link']

		if link != "":
			description = f"**[{activity}]({link})**"
		else:
			description = f"**{activity}**"
		embed = discord.Embed(title=f"Type of activity: {type_}", description=description)
		await ctx.send(embed=embed)

	@commands.command(name="cat", aliases=["catto", "kitten", "kitty", "meow"], brief="Get Catto pics UwU")
	async def catto(self, ctx):
		resp = requests.get("https://api.thecatapi.com/v1/images/search").json()
		url = resp[0]["url"]

		embed = discord.Embed(title="Here's your catto uwu")
		embed.set_image(url=url)

		await ctx.send(embed = embed)

def setup(bot):
	bot.add_cog(fun(bot))
