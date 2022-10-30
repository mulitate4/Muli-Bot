import discord
from discord.ext import commands
from other_modules import get_latest_post_data

class OwnerCog(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(name="new_article", aliases=["article", "new_post"], hidden=True)
	@commands.is_owner()
	async def new_article_alert(self, ctx, link:str="", no_of_paras=1):
		response = get_latest_post_data.get_all_data(link, no_of_paras)
		if response == False:
			return

		title, desc, image_url, link = response
		alert = "Read More at: " + link + " @everyone"
		new_article_embed = discord.Embed(title=title, description=desc+"\n"+alert)

		new_article_embed.set_image(url=image_url)
		new_article_embed.set_footer(text="Author: MUwUlitate4#9118")

		await ctx.send(embed=new_article_embed)
		await ctx.send("@everyone")

	@commands.command(name='load', hidden=True)
	@commands.is_owner()
	async def load(self, ctx, *, cog:str):
		cogstr = "cogs." + cog
		try:
			self.bot.load_extension(cogstr)
		except Exception as e:
			await ctx.send(f'--Error--\n{type(e).__name__} - {e}')
		else:
			await ctx.send('--Success!--')
	
	@commands.command(name='unload', hidden=True)
	@commands.is_owner()
	async def unload(self, ctx, *, cog:str):
		cogstr = "cogs." + cog
		try:
			self.bot.unload_extension(cogstr)
		except Exception as e:
			await ctx.send(f'--Error--\n{type(e).__name__} - {e}')
		else:
			await ctx.send('--Success!--')

	@commands.command(name='reload', hidden=True)
	@commands.is_owner()
	async def reload(self, ctx, *, cog:str):
		cogstr = "cogs." + cog
		try:
			self.bot.reload_extension(cogstr)
		except Exception as e:
			await ctx.send(f'--Error--\n{type(e).__name__} - {e}')
		else:
			await ctx.send('--Success!--')
		
	@commands.command(name="dm", hidden=True, brief="Dms a user")
	@commands.is_owner()
	async def dm(self, ctx, member: discord.Member, *, message):
		await member.send(message)

def setup(bot):
	bot.add_cog(OwnerCog(bot))