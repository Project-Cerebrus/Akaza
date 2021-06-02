import discord, os

class Config:
	PREFIX = ["dd?", "doggo ", ",","="]
	BOT_TOKEN = os.environ["TOKEN"]
	CURRENCY_NAME = "DoggoCoins"
	CURRENCY_ICON = "Ⓓ"
	COLOR_THEME = discord.Color.dark_red()
class Emotes:
	w_arrow = 849131436865749032
	p_arrow = 849135000406589500

class Roles:
	ADMIN = [824784517541134386, 824626266094305331, 824626336558743603, 824628347715321866]
	MOD = [824634080192757831, 824633245278535700]
	DEVS = [775198018441838642, 746904488396324864]
	MUTEROLE = 824673580935282699
	BOTMODS = ADMIN + MOD + DEVS
	STAFF = 825060038019907706

class Getters:
	def get_usage_status(ctx):
		if ctx.channel.id not in Channels.ALLOWED:
			if ctx.author.id in Roles.BOTMODS:
				return True
			return False
		else:
			return True

class Channels:
	ALLOWED = [847409923166830612,824642144240271400,824642277883510824,825019626698047508]