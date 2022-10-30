import discord
from discord.ext import commands
from googleapiclient import discovery
from other_modules import api_secrets
import requests

_yt_api_key = api_secrets.yt_api_key

youtube = discovery.build('youtube',
				'v3',
				developerKey=_yt_api_key
				)

class info(commands.Cog):
	description = "Commands that give you information!"

	def __init__(self, bot):
		self.bot = bot

	def youtube_channel_search(self, query):
		channel_req = youtube.search().list(q=query, part='snippet', type='channel', maxResults=1)
		channel_resp = channel_req.execute()
		channel_info = channel_resp['items'][0]['snippet']

		channel_id = channel_info['channelId']
		channel_name = channel_info['title']
		channel_logo = channel_info['thumbnails']['medium']['url']
		channel_desc = channel_info['description']
		channel_createdAt = channel_info['publishedAt']

		channel_stats = requests.get("https://www.googleapis.com/youtube/v3/channels?part=statistics&id="+channel_id+"&key="+_yt_api_key).json()
		channel_subs = channel_stats['items'][0]['statistics']['subscriberCount']

		youtube_embed = discord.Embed(title=channel_name, description=channel_desc)
		youtube_embed.set_thumbnail(url=channel_logo)
		youtube_embed.add_field(name="Subscribers: ", value=channel_subs, inline=True)
		youtube_embed.add_field(name="Channel Created At", value=channel_createdAt, inline=True)
		return youtube_embed

	def youtube_video_search(self, query):
		vid_req = youtube.search().list(q=query, type='video', maxResults=1, part='snippet')
		vid_resp = vid_req.execute()
		video = vid_resp['items'][0]['snippet']

		video_id = vid_resp['items'][0]['id']['videoId']
		video_url = ("https://www.youtube.com/watch?v=" + video_id)

		video_title = video['title']
		video_desc = video['description']
		video_channel = video['channelTitle']
		video_publishedAt = video['publishTime']

		video_embed = discord.Embed(Title=video_title, description=video_desc)
		video_embed.add_field(name="Video: ", value="[Open In Browser]("+video_url+")", inline=False)
		video_embed.add_field(name="channel: ", value=video_channel, inline=True)
		video_embed.add_field(name="Publish Time: ", value=video_publishedAt, inline=True)
		return video_url, video_embed

	def get_corona_stats(self, country=""):
		if country == "":
			cor_req = requests.get('https://disease.sh/v3/covid-19/all').json()
			cor_embed = discord.Embed(title="Global Corona Cases", description="Global Info about Covid-19")
		else:
			cor_req = requests.get(f'https://disease.sh/v3/covid-19/countries/{country}').json()
			country_name = cor_req["country"]

			cor_embed = discord.Embed(title=f"{country_name} Corona Cases", description=f"Info about Covid-19 in {country_name}")
		
		cor_total_cases = cor_req["cases"]
		cor_today_cases = cor_req["todayCases"]
		cor_total_recovered = cor_req["recovered"]
		cor_today_recovered = cor_req["todayRecovered"]
		cor_critical = cor_req['critical']

		cor_embed.add_field(name="Total covid-19 cases: ", value=cor_total_cases, inline=True)
		cor_embed.add_field(name="Total covid-19 recovered: ", value=cor_total_recovered, inline=True)
		
		cor_embed.add_field(name='.', value='.', inline=True)

		cor_embed.add_field(name="Today covid-19 cases: ", value=cor_today_cases, inline=True)
		cor_embed.add_field(name="Today covid-19 recovered: ", value=cor_today_recovered, inline=True)		
		cor_embed.add_field(name="Critical covid-19 cases: ", value=cor_critical, inline=True)
		return cor_embed

	@commands.command(name="invite", aliases=["invite_bot"])
	async def invite_bot(self, ctx):
		await ctx.send("invite this bot to your server using this link -\n <https://discord.com/api/oauth2/authorize?client_id=717419474806112338&permissions=2146958423&scope=bot>\nSupport Server: https://discord.gg/9CBrq6D")


	@commands.command(name='youtube_channel', aliases=['subs', 'yt_channel', 'channel'], briefs="gets info about channel such as subscribers")
	async def youtube_channel(self, ctx, *, channel):
		result = self.youtube_channel_search(channel)
		await ctx.send(embed=result)

	@commands.command(name='youtube_video', aliases=['yt_video', 'video_search', 'video'], brief="Searches a video, and gets the first result from youtube")
	async def yt_video_search(self, ctx, *, q: str):
		final_video_url, final_video_embed = self.youtube_video_search(q)
		await ctx.send(final_video_url)
		await ctx.send(embed = final_video_embed)

	@commands.command(name='server_info', aliases=['server', 'server_stats'], brief="Gets the server's statistics")
	@commands.guild_only()
	async def server_stats(self, ctx):
		guild = ctx.guild

		roles = str(len(guild.roles))
		emojis = str(len(guild.emojis))
		channels = str(len(guild.channels))

		embeded = discord.Embed(title=guild.name, description='guild Info', color=0xEE8700)
		embeded.set_thumbnail(url=guild.icon_url)
		embeded.add_field(name="Created on:", value=guild.created_at.strftime('%d %B %Y at %H:%M UTC+3'), inline=False)
		embeded.add_field(name="guild ID:", value=guild.id, inline=False)
		embeded.add_field(name="Users on guild:", value=guild.member_count, inline=True)
		embeded.add_field(name="guild owner:", value=guild.owner, inline=True)

		embeded.add_field(name="guild Region:", value=guild.region, inline=True)
		embeded.add_field(name="Verification Level:", value=guild.verification_level, inline=True)

		embeded.add_field(name="Role Count:", value=roles, inline=True)
		embeded.add_field(name="Emoji Count:", value=emojis, inline=True)
		embeded.add_field(name="Channel Count:", value=channels, inline=True)
		await ctx.send(embed=embeded) 

	@commands.command(name="corona", aliases=["corona_stats"], brief="Leave blank after command to get Global stats, or give a country to get country's stats")
	async def corona_stats(self, ctx, country=""):
		await ctx.send(embed=self.get_corona_stats(country))

def setup(bot):
	bot.add_cog(info(bot))
