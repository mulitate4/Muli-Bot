# TODO: Add songs to a dict, then pop the songs after they are complete 
# TODO: ADD QUEUE - Dict{"GUILD_ID": [ARRAY]}

import discord
from discord.ext import commands
import asyncio

import youtube_dl
from googleapiclient import discovery
import requests

import os
import collections

from other_modules import api_secrets

_yt_api_key = api_secrets.yt_api_key

youtube = discovery.build('youtube',
				'v3',
				developerKey=_yt_api_key
				)

ydl_opts = {
	'format': 'bestaudio/best',
	'keepvideo': False,
	'outtmpl': '%(id)s.webm',
}

players = {}
songs_list = collections.defaultdict(list)



class MusicPlayer():
	def __init__(self, ctx):
		pass

class music(commands.Cog):
	description = "Music Commands, Epic features like queue!"
	def __init__(self, bot):
		self.bot = bot
		

	def song_dload(self, query):
		vid_req = youtube.search().list(q=query, type='video', maxResults=1, part='snippet')
		vid_resp = vid_req.execute()
		video = vid_resp['items'][0]['snippet']

		video_id = vid_resp['items'][0]['id']['videoId']
		video_title = video['title']

		video_url = ("https://www.youtube.com/watch?v=" + video_id)

		with youtube_dl.YoutubeDL(ydl_opts) as ydl:
			ydl.download([video_url])
		return video_id, video_title, video_url

	def get_voice_client(self, server):
		voice_client = None
		for index, client in enumerate(self.bot.voice_clients):
			if client.guild == server:
				voice_client = self.bot.voice_clients[index]
		
		return voice_client

	async def play_song(self, query, ctx):

		server = ctx.message.guild
		voice_client = self.get_voice_client(server)

		next = asyncio.Event()

		await self.bot.wait_until_ready()

		global vid_title, vid_url
		vid_id, vid_title, vid_url = self.song_dload(query)

		song_embed = discord.Embed(title="Now Playing:", description=f"**[{vid_title}]({vid_url})**")
		await ctx.send(embed=song_embed)


		voice_client.play(discord.FFmpegPCMAudio(source=vid_id+".webm"), after=lambda _: self.bot.loop.call_soon_threadsafe(next.set()))
		voice_client.source = discord.PCMVolumeTransformer(voice_client.source)
		voice_client.volume = 0.5

		await next.wait()
		songs_list[server.id].pop(0)
		os.remove(vid_id+".webm")

		vid_title = ""
		if songs_list[server.id] == []:
			return 
		print("bruh")

	@commands.command(name="play", aliases=['p'], brief="Makes Muli-bot play music")
	@commands.guild_only()
	async def play(self, ctx, *,query):

		server = ctx.message.guild
		voice_client = self.get_voice_client(server)
		songs_list[server.id].append(query)
		
			#====== JOIN VOICE CHANNEL ======#
		#Checks if bot is already in Voice Channel
		if voice_client == None:
			#Checks if usr is in Voice Channel
			if ctx.message.author.voice != None:
				channel = ctx.message.author.voice.channel
				await channel.connect()
				voice_client = self.get_voice_client(server)
			else:
				await ctx.send("Join a Voice Channel dummy.")
				return


		if voice_client.is_playing() or voice_client.is_paused():
			await ctx.send(embed=discord.Embed(title="Queued Song!"))
		else:
			while songs_list[server.id] != []:
				await self.play_song(songs_list[server.id][0], ctx)

	@commands.command(name="join", aliases=["summon"], brief="Makes Muli-bot join a Voice channel")
	@commands.guild_only()
	async def join(self, ctx):
		channel = ctx.message.author.voice
		if channel != None:
			channel = ctx.message.author.voice.channel
			await channel.connect()
			return 
		await ctx.send("Join a Voice Channel dummy.")

		vc = ctx.voice_client

		if vc:
			if vc.channel.id == channel.id:
				return
			try:
				await vc.move_to(channel)
			except asyncio.TimeoutError:
				pass
		else:
			try:
				await channel.connect()
			except asyncio.TimeoutError:
				pass

		await ctx.send(f'Connected to: **{channel}**', delete_after=20)

	@commands.command(name="disconnect", aliases=["leave", 'fuckoff', 'dc'], brief="Makes Muli-bot leave a Voice channel")
	@commands.guild_only()
	async def disconnect(self, ctx):
		server = ctx.message.guild
		
		voice_client = self.get_voice_client(server)

		songs_list[server.id] = []
		voice_client.stop()
		await voice_client.disconnect()

	@commands.command(name="pause", brief="Pause the currently playing track")
	@commands.guild_only()
	async def pause(self, ctx):
		server = ctx.message.guild
		voice_client = self.get_voice_client(server)

		if not voice_client:
			await ctx.send("Join a Voice Channel BRUH.")
			return

		pause_embed = discord.Embed(title="Paused Song")

		await ctx.send(embed=pause_embed)
		voice_client.pause()

	@commands.command(name="resume", aliases=['unpause'], brief="Resume the currently playing track")
	@commands.guild_only()
	async def resume(self, ctx):
		server = ctx.message.guild
		voice_client = self.get_voice_client(server)

		if not voice_client:
			await ctx.send("Join a Voice Channel BRUH.")
			return 

		resume_embed = discord.Embed(title="Resumed Song")

		await ctx.send(embed=resume_embed)
		voice_client.resume()

	@commands.command(name="skip", brief="Skips the currently playing track")
	@commands.guild_only()
	async def skip(self, ctx, n:int=1):
		server = ctx.message.guild
		voice_client = self.get_voice_client(server)

		if not voice_client:
			await ctx.send("Join a Voice Channel BRUH.")
			return

		for i in range(n):
			voice_client.stop()
			asyncio.sleep(0.1)

		skipped_embed = discord.Embed(title="Skipped Song")
		await ctx.send(embed=skipped_embed)
		voice_client.resume()

	@commands.command(name="queue", aliases=['q', 'que'], brief="Sends the currently queued songs")
	@commands.guild_only()
	async def queue(self, ctx):
		server = ctx.message.guild
		voice_client = self.get_voice_client(server)

		if not voice_client:
			await ctx.send("Join a Voice Channel BRUH.")
			return 

		if not voice_client.is_playing():
			queue_embed = discord.Embed(title="Not playing anything currently!")
			await ctx.send(embed=queue_embed)
			return 

		q_str = "\n".join([song for song in songs_list[server.id]])
		queue_embed = discord.Embed(title="Currently queued songs:", description=q_str)
		await ctx.send(embed=queue_embed)

	@commands.command(name="stop", brief="Skips the currently playing track")
	@commands.is_owner()
	async def stop(self, ctx):
		server = ctx.message.guild
		voice_client = self.get_voice_client(server)

		voice_client.stop()

	@commands.command(name="lyr", aliases=["lyrics"], brief="Skips the currently playing track")
	async def lyrics(self, ctx):
		server = ctx.message.guild
		voice_client = self.get_voice_client(server)
		curr_song = songs_list[server.id][0]

		if not voice_client:
			await ctx.send("Join a Voice Channel BRUH.")
			return 

		lyrics = requests.get(r"https://lyricist-app-banckend.herokuapp.com/?q="+curr_song)
		if lyrics.status_code == 503:
			await ctx.send("Couldn't retrieve song, try again")
			return
		
		if lyrics.text == "couldn't retrieve song":
			await ctx.send("couldn't find the song")

		else:
			embed = discord.Embed(title=f"{curr_song}", description=lyrics.text)
			await ctx.send(embed=embed)



def setup(bot):
	bot.add_cog(music(bot))