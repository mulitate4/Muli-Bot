import discord
from discord.ext import commands
from other_modules import dank_space

class games(commands.Cog):
	description = "Games to play on Discord itself!"
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="dank_space", brief='''
		A dank space adventure text-based game, 
		where things never go as expected.
		A Work in Progress.
	''')
	async def text_game(self, ctx):
		adv = dank_space.dank_space_adv()
		await ctx.send(embed=adv.start())

		def checkabc(m):
			return (m.content.lower() == 'a' or m.content.lower() == 'b' or m.content.lower() == 'c' or m.content.lower() == 'quit') and m.channel == ctx.channel and m.author == ctx.author

		def checkleftright(m):
			return (m.content.lower() == 'left' or m.content.lower() == 'right' or m.content.lower() == 'l' or m.content.lower() == 'r' or m.content.lower() == 'quit') and m.channel == ctx.channel and m.author == ctx.author

		msg = await self.bot.wait_for('message', check=checkleftright, timeout=30.0)
		msg = msg.content.lower()

		if msg == 'right':
			await ctx.send(embed=adv.a1_right())

			choice = await self.bot.wait_for('message', check=checkabc, timeout=30.0)
			choice = choice.content.lower()
			await ctx.send(embed=adv.a1_right_choice(choice))

			if choice == 'a':
				return "stopped"

			await ctx.send(embed = adv.a1_continued())
			choice2 = await self.bot.wait_for('message', check=checkabc, timeout=30.0)
			choice2 = choice2.content.lower()
			await ctx.send(embed = adv.a2_right_choice(choice2))

			if choice2 == 'a' or choice2 == 'b':
				return "stopped"

			await ctx.send('```work in progress```')


		elif msg == 'left':
			await ctx.send(embed = adv.b1_left())

			choice = await self.bot.wait_for('message', check=checkabc, timeout=30.0)
			choice = choice.content.lower()
			await ctx.send(embed = adv.b1_left_choice(choice))

			await ctx.send(embed = adv.b1_continued())

			choice2 = await self.bot.wait_for('message', check=checkabc, timeout=30.0)
			choice2 = choice2.content.lower()
			await ctx.send(embed = adv.b2_left_choice(choice2))
			if choice2 == 'a' or choice2 == 'b':
				return "stopped"

			await ctx.send('```work in progress```')

		elif msg.content.lower() == 'quit':
			await  ctx.send("``` ----- you quit the game ----- ```")
			return "stopped"

def setup(bot):
	bot.add_cog(games(bot))