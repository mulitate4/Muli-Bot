import random
import discord

class dank_space_adv:
	choice_list = []
	def start(self):
		game_str = '''You work at a space station, it's been almost two months,and you are supposed to return back to earth. Suddenly, a HUGE alien ship appears outta nowhere. Your crewmates literally died, and you are the only one left (of course you are). You see two passageways, one goes left and the other, right. What do you do?'''
		game_embed = discord.Embed(title="Start", description=game_str)
		game_str_option = '''Left \nRight \n\nType left or right in chat'''
		game_embed.add_field(name="Choice", value=game_str_option, inline=False)
		return game_embed

	def a1_right(self):
		game_str = '''You walk the right pathway and encounter a wild cafeteria, what will you do?'''
		game_embed = discord.Embed(title="Right", description=game_str)
		game_str_option = '''a)eat hamborgor \nb)throw pokeball \nc)run away \n\nType your letter choice in chat'''
		game_embed.add_field(name="Choice", value=game_str_option, inline=False)
		return game_embed

	def a1_right_choice(self, choice):
		if choice == 'a':
			game_str = "You eat the borgor and die. That Borgor was probably like 10 months old.(wasted)"
			return discord.Embed(title="You Ded Lmao", description=game_str)

		elif choice == 'b':
			rand = random.randint(1,2)
			if rand == 1:
				game_str = "You throw a pokeball and catch a wild pizza, WTF? what were you thinking? You walk away with a pokeball"
			if rand == 2:
				game_str = "You throw a pokeball and try to catch a wild pizza, but it escapes, now you are hungry and down a pokeball"
			return discord.Embed(title="Pokeball BRUH moment", description=game_str)

		elif choice == 'c':
			game_str = "What a sissy, You just ran away from a cafeteria???"
			return discord.Embed(title="Sissy LMAO", description=game_str)

	def a1_continued(self):
		game_str = '''You continue onwards on the right passagway, when, out of nowhere, you see a green alien fighting a purple alien. The green alien swallows the purple alien whole. (Excuse me what the hecc?) You randomly find a gun on you with 2 bullets left. What d o you d o ?'''
		game_embed = discord.Embed(title="Right continued", description=game_str)
		game_str_option = '''a)Shoot it with your gun. \nb)Hit it with your gun. \nc)Literally walk around it. \n\nType your choice in chat'''
		game_embed.add_field(name="Choice", value=game_str_option, inline=False)
		return game_embed

	def a2_right_choice(self, choice):
		if choice == 'a':
			game_str ='''You shoot it with your gun, but realize you are in space, and the recoil sends you flying back and you get impaled by a spear. OOF (who even put that there?).'''
			return discord.Embed(title="You Ded Lmao", description=game_str)

		elif choice == 'b':
			game_str = '''You try to hit it, but it swallows both you and the gun w h o l e. You just saw it eating a whole other alien, what were you thinking? LMAO'''
			return discord.Embed(title="You Ded Lmao", description=game_str)

		elif choice == 'c':
			game_str = '''You literally walk around it, cause its slow AF, and you live (BRUH moment).'''
			return discord.Embed(title="You walk around, BRUH moment", description=game_str)



	def b1_left(self):
		game_str = "You go on the left passageway and see a bathroom, but you dont really need to poop right now. What d o you d o?"
		game_embed = discord.Embed(title="Left", description=game_str)
		game_str_option = '''a)Force it out \nb)Stare at it's beauty \nc)Walk away bruh \n\nType your letter choice in chat'''
		game_embed.add_field(name="Choice", value=game_str_option, inline=False)
		return game_embed

	def b1_left_choice(self, choice):
		if choice == 'a':
			game_str ='''You sit there for 10 minutes straight, thinking about life, trying to force out poop. Then you ask yourself, \" what am i doing? \" You get up and continue.'''
			return discord.Embed(title="You sit down", description=game_str)

		elif choice == 'b':
			game_str = '''\"I've been looking at this for 5 hours minutes now, It's beautiful.\"(If you dont get this meme, i dont know what to say :|)'''
			return discord.Embed(title="You stare at it", description=game_str)

		elif choice == 'c':
			game_str = '''You walk away like a normal person.'''
			return discord.Embed(title="You walk away", description=game_str)

	def b1_continued(self):
		game_str = '''You coninue onwards when suddenly you see a purple alien swallowing a green alien whole and its coming for you next. What d o you d o?'''
		game_embed = discord.Embed(title="Left continued", description=game_str)
		game_str_option = '''a)Try to walk around it \nb)Play dead \nc)Stand Still \n\nType your choice in chat'''
		game_embed.add_field(name="Choice", value=game_str_option, inline=False)
		return game_embed

	def b2_left_choice(self, choice):
		if choice == 'a':
			game_str ='''You try to walk around it, but its fast AF, and it swallows you. LMAO'''
			return discord.Embed(title="You DED LMAO", description=game_str)

		elif choice == 'b':
			game_str = '''You play you ded, but your L O U D breathing gives you away, and you are eaten up by the alien.(plus its an alien not a bear what were you thinking?)'''
			return discord.Embed(title="You DED LMAO", description=game_str)

		elif choice == 'c':
			game_str = '''You stand still. You stand so still, that you become invisible to the naked eye. The alien wonders where you went, and moves on to the next alien.'''
			return discord.Embed(title="You Stand STILL", description=game_str)