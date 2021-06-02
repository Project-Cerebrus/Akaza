# copyright Eris 2021 without this this code is fully illegal

import discord, random
from discord.ext import commands
import os
import subprocess
from discord.utils import get
import asyncio
from io import StringIO
import json
import sys
import datetime
from discord import Member
from discord import Embed,File
from typing import Optional
from random import choice
from asyncio import TimeoutError, sleep
async def checkreq(users,reqrole,checkmsg,prize,author,ctx):
	for item in users:
		if reqrole not in item.roles and reqrole != "None":
			await checkmsg.remove_reaction("🎉",item)
			embed= discord.Embed(title="Required role",description=f"please get **{reqrole.name}** role for {prize} by {author.name} in {ctx.guild.name}",color=item.color)
			await item.send(embed=embed)
def convert(time):
		pos = ["s","m","h","d"]

		time_dict = {"s" : 1, "m" : 60, "h" : 3600 , "d" : 3600*24}

		unit = time[-1]

		if unit not in pos:
				return -1
		try:
				val = int(time[:-1])
		except:
				return -2
		return val * time_dict[unit]
devs = ['775198018441838642', '746904488396324864', '750755612505407530']

class giveaways(commands.Cog, name='giveaways'):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(aliases=["gcommands"])
	async def license(self,ctx):
		embed = discord.Embed(title="Giveaways commands",description="This was taken from project cerebus made by @Eris#5528\ngstart - start a giveaway\ngend - end a giveaway\ngcreate - create a giveaway\ngreroll - reroll a giveaway\n**Synatx:**\nthe commands work like this:\ngstart <time> <prize>\ngreroll <channelid> <messageid>\n you can get the ids by copying the message link and getting the last 2 ids")
		await ctx.send(embed=embed)
	#@commands.command(aliases=["rmi"])
	#async def remind(self,ctx,time,*,msg:str):
		#asynctime = convert(time)
		#asynctime = int(asynctime)
		#await ctx.send("reminder set")
		#await asyncio.sleep(asynctime)
		#await ctx.author.send(msg)
	@commands.command()
	async def gstart(self,ctx,time,reqrole, * , prize: str):
		reqid = reqrole
		if reqrole == "none":
			reqrole = "None"
			reqid = "None"
		if reqrole != "None":
			reqrole = int(reqrole)
			reqrole = ctx.guild.get_role(reqrole)
			reqid = reqrole.mention
		asynctime = convert(time)
		asynctime = int(asynctime)
		await ctx.message.delete()		
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.message.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			alpha = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
			gawid = random.choice(alpha) + random.choice(alpha) + random.choice(alpha) + random.choice(alpha) + random.choice(alpha)
			with open("data/gaw.json","r") as f:
				gaw = json.load(f)
			
			timez = asynctime
			comment = f"**{timez}** second(s) from now!"
			if timez > 60:
				timez = float(timez) / 60
				timez = round(timez)
				comment = f"**{timez}** minute(s) from now!"
			if timez > 3600:
				timez = float(timez) / 3600
				timez = round(timez)
				comment = f"**{timez}** hour(s) from now!"
			if timez > 86400:
				timez = float(timez) / 86400
				timez = round(timez)
				comment = f"**{timez}** day(s) from now!"			
			embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
			end = datetime.datetime.utcnow() + datetime.timedelta(seconds = timez)
			embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
			end = datetime.datetime.utcnow() + datetime.timedelta(seconds = timez)
			embed.add_field(name = f"Ends at:", value = comment)
			embed.add_field(name = "Requirement:", value = f"{reqid}")
			embed.add_field(name = "By:", value = f"{ctx.author.mention}",inline=False)
			embed.add_field(name = "Id:", value = f"{gawid}",inline=True)
			embed.set_footer(text = f"Ends At: {end} UTC")
			embed.set_thumbnail(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")
			my_msg = await ctx.send(embed = embed)
			gaw[str(my_msg.id)] = {}
			gaw[str(my_msg.id)]["guild"] = ctx.guild.id
			gaw[str(my_msg.id)]["time"] = asynctime
			gaw[str(my_msg.id)]["author"] = ctx.author.id
			gaw[str(my_msg.id)]["req"] = reqid
			gaw[str(my_msg.id)]["prize"] = prize
			gaw[str(my_msg.id)]["channel"] = ctx.channel.id
			gaw[str(my_msg.id)]["gawid"] = gawid
			gaw[str(my_msg.id)]["msgid"] = my_msg.id
			with open("data/gaw.json","w") as z:
				json.dump(gaw,z)
			with open("data/gawid.json","w") as zk:
				json.dump(gaw,zk)
			await my_msg.add_reaction("🎉")
			item = str(my_msg.id)
			guildid = gaw[item]["guild"]
			authorid = gaw[item]["author"]
			guild = self.bot.get_guild(guildid)
			reqid = gaw[item]["req"]
			prize = gaw[item]["prize"]
			channelid = gaw[item]["channel"]
			author = self.bot.get_user(authorid)
			channel = guild.get_channel(int(channelid))
			gawid = gaw[item]["gawid"]
			msgid = gaw[item]["msgid"]
			new_msg = await channel.fetch_message(msgid)
		if reqid != "None":
			reqid = f"<@{reqid}>"
		while timez > 0:
			await asyncio.sleep(1)
			gaw[item]["time"] -= 1
			with open("data/gaw.json","w") as gawz:
				json.dump(gaw,gawz)
			checkmsg = await channel.fetch_message(msgid)
			users = await checkmsg.reactions[0].users().flatten()
			users.pop(users.index(self.bot.user))
			await checkreq(users,reqrole,checkmsg,prize,author,ctx)
			timez = gaw[item]["time"]
			comment = f"**{timez}** second(s) from now!"
			if timez > 60:
				timez = float(timez) / 60
				timez = round(timez)
				comment = f"**{timez}** minute(s) from now!"
			if timez > 3600:
				timez = float(timez) / 3600
				timez = round(timez)
				comment = f"**{timez}** hour(s) from now!"
			if timez > 86400:
				timez = float(timez) / 86400
				timez = round(timez)
				comment = f"**{timez}** day(s) from now!"			
			embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)
			end = datetime.datetime.utcnow() + datetime.timedelta(seconds = timez)
			embed.add_field(name = f"Ends at:", value = comment)
			embed.add_field(name = "Requirement:", value = f"{reqid}")
			embed.add_field(name = "By:", value = f"{author.mention}",inline=False)
			embed.add_field(name = "Id:", value = f"{gawid}")
			embed.set_footer(text = f"Ends At: {end} UTC")
			embed.set_thumbnail(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")
			await new_msg.edit(embed=embed)
			if timez == 0:
					winner = "Unable to get winner"
					winnerz = True
					try:
						embed = discord.Embed(title="You Won",description=f"**Prize:** {prize}\n**Author:** {ctx.author.name}")
						await checkreq(users,reqrole,checkmsg,prize,author,ctx)
						latestmsg = await channel.fetch_message(msgid)
						users = await latestmsg.reactions[0].users().flatten()
						users.pop(users.index(self.bot.user))
						winner = random.choice(users)
					except IndexError:
						await new_msg.reply("No one reacted to this giveaway")
						winnerz = False
					if winnerz == False:
						return
					else:
						embed = discord.Embed(title="Giveaway Over",description=f"{winner.mention} won {prize}",color=winner.color)
						await author.send(embed=embed)
						await latestmsg.reply(f"{winner.mention} won {prize}")
						embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = author.color)
						embed.add_field(name = f"Winner:", value = f"{winner.mention}")
						embed.add_field(name = "Requirement:", value = f"{reqid}")
						embed.add_field(name = "By:", value = f"{author.mention}",inline=False)
						embed.add_field(name = "Id:", value = f"{gawid}",inline=True)
						embed.set_footer(text = f"Ended")
						embed.set_thumbnail(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")
						await latestmsg.edit(embed=embed)
						winbed = discord.Embed(title="You Won",description=f"You won {prize} in {guild.name}\nDM {author.name} for your prize if not already paid",color=author.color)
						await winner.send(embed=winbed)
					del gaw[item]
					with open("data/gaw.json","w") as gawz:
						json.dump(gaw,gawz)
					return
	@commands.command(name="giftdel", aliases=["gcancel", "gftdel", "gdl"])
	async def gstop(self, ctx,gawid,reason):
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.message.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			with open("data/gawid.json","r") as z:
				gawidz = json.load(z)
			for item in gawidz:
				if gawid == gawidz[item]["gawid"]:
					guildid = gawidz[item]["guild"]
					authorid = gawidz[item]["author"]
					guild = self.bot.get_guild(guildid)
					reqid = gawidz[item]["req"]
					prize = gawidz[item]["prize"]
					channelid = gawidz[item]["channel"]
					author = self.bot.get_user(authorid)
					channel = guild.get_channel(int(channelid))
					gawid = gawidz[item]["gawid"]
					msgid = gawidz[item]["msgid"]
					if ctx.guild.id != guildid:
						return await ctx.send("This is from a different guild please use it in that guild")
					if ctx.author.id != authorid:
						return await ctx.send(f"You need to be the author of this gaw : {author.name}")
					id = True
				else:
					if id != True:
						id = False
			try:
					if id == False:
						return await ctx.send("unable to get id")
					msg = await channel.fetch_message(msgid)
					newEmbed = Embed(title="Giveaway Cancelled", description=f"The giveaway has been cancelled!!\n **Reason:** {reason}")
					#Set Giveaway cancelled
					self.cancelled = True
					await msg.edit(embed=newEmbed) 
			except:
					embed = Embed(title="Failure!", description="Cannot cancel Giveaway")
					await ctx.send(emebed=embed)
					return
		else:
			await ctx.send("missing permissions, required premissons are manage_channels or administrator")

	@commands.command()
	async def gcreate(self,ctx):
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.message.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")

			questions = ["Which channel should it be hosted in?", 
									"What should be the duration of the giveaway? (s|m|h|d)",
									"What is the prize of the giveaway?"]

			answers = []

			def check(m):
					return m.author == ctx.author and m.channel == ctx.channel 

			for i in questions:
					await ctx.send(i)

					try:
							msg = await self.bot.wait_for('message', timeout=15.0, check=check)
					except asyncio.TimeoutError:
							await ctx.send('You didn\'t answer in time, please be quicker next time!')
							return
					else:
							answers.append(msg.content)
			try:
					c_id = int(answers[0][2:-1])
			except:
					await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
					return

			channel = self.bot.get_channel(c_id)

			time = convert(answers[1])
			if time == -1:
					await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
					return
			elif time == -2:
					await ctx.send(f"The time must be an integer. Please enter an integer next time")
					return            

			prize = answers[2]

			await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")


			embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = ctx.author.color)

			embed.add_field(name = "Hosted by:", value = ctx.author.mention)

			embed.set_footer(text = f"Ends {answers[1]} from now!")
			embed.set_thumbnail(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")

			my_msg = await channel.send(embed = embed)


			await my_msg.add_reaction("🎉")


			await asyncio.sleep(time)


			new_msg = await channel.fetch_message(my_msg.id)


			users = await new_msg.reactions[0].users().flatten()
			users.pop(users.index(self.bot.user))

			winner = random.choice(users)

			await channel.send(f"Congratulations! {winner.mention} won {prize}!")
			await winner.send(f"You won a giveaway")
		else:
			await ctx.send("missing permissions, required premissons are manage_channels or administrator")
	@commands.command(aliases=["gend"])
	async def greroll(self,ctx, gawid):
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.message.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			id = None
			with open("data/gawid.json","r") as z:
				gawidz = json.load(z)
			for item in gawidz:
				if gawid == gawidz[item]["gawid"]:
					guildid = gawidz[item]["guild"]
					authorid = gawidz[item]["author"]
					guild = self.bot.get_guild(guildid)
					reqid = gawidz[item]["req"]
					prize = gawidz[item]["prize"]
					channelid = gawidz[item]["channel"]
					channel = guild.get_channel(int(channelid))
					gawid = gawidz[item]["gawid"]
					msgid = gawidz[item]["msgid"]
					if ctx.guild.id != guildid:
						return await ctx.send("This is from a different guild please use it in that guild")
					if ctx.author.id != authorid:
						return await ctx.send(f"You need to be the author of this gaw : <@{authorid}>")
					id = True
				else:
					if id != True:
						id = False
			try:
					if id == False:
						return await ctx.send("unable to get id")
					new_msg = await channel.fetch_message(msgid)
			except:
					await ctx.send("The id was entered incorrectly.")
					return
			reqrole = "None"
			if reqid != "None":
				reqrole = ctx.guild.get_role(reqid)
			author =  self.bot.get_user(authorid)
			users = await new_msg.reactions[0].users().flatten()
			users.pop(users.index(self.bot.user))
			await checkreq(users,reqrole,new_msg,prize,author,ctx)

			winner = random.choice(users)

			await new_msg.reply(f"Congratulations! The new winner is {winner.mention}.!") 
			winbed = discord.Embed(title="You Won",description=f"You won {prize} in {guild.name}\nDM {author.name} for your prize if not already paid",color=author.color)
			await winner.send(embed=winbed)
		else:
			await ctx.send("missing permissions, required premissons are manage_channels or administrator")
	@commands.command()
	async def ginfo(self,ctx,gawid):
	"""
	@commands.command(name="giftrrl", aliases=["gifreroll", "greroll", "grr","gend"])
	async def gawend(self, ctx, channel : discord.TextChannel, id_: int):
		role = discord.utils.find(lambda r: r.name == '・Giveaway Manager', ctx.message.guild.roles)
		role2 = discord.utils.find(lambda r: r.name == 'Giveaway Manager', ctx.message.guild.roles)
		role3 = discord.utils.find(lambda r: r.name == 'Giveaways Manager', ctx.message.guild.roles)
		if ctx.author.guild_permissions.manage_channels == True or ctx.author.guild_permissions.administrator == True or role in ctx.author.roles or role2 in ctx.author.roles or role3 in ctx.author.roles:
			try:
					msg = await channel.fetch_message(id_)
			except:
					await ctx.send("The channel or ID mentioned was incorrect")
			users = await msg.reactions[0].users().flatten()
			if len(users) <= 0:
					emptyEmbed = Embed(title="Giveaway Time !!",
																	description=f"Win a Prize today")
					emptyEmbed.add_field(name="Hosted By:", value=ctx.author.mention)
					emptyEmbed.set_footer(text="No one won the Giveaway")
					await msg.edit(embed=emptyEmbed)
					return
			if len(users) > 0:
					winner = choice(users)
					winnerEmbed = Embed(title="Giveaway Time !!",
															description=f"Win a Prize today",
															colour=0x00FFFF)
					winnerEmbed.add_field(name=f"Congratulations On Winning Giveaway", value=winner.mention)
					winnerEmbed.set_image(url="https://i.pinimg.com/originals/eb/2a/8f/eb2a8f4ddfb50c23712a3cd0d5cc2a3a.gif")
					await msg.edit(embed=winnerEmbed)
					await channel.send(f"Congratulations! The new winner is {winner.mention}.!")
					await winner.send(f"You won a giveaway")
					return
		else:
			await ctx.send("missing permissions, required premissons are manage_channels or administrator")
							# users.pop(users.index(self.bot.user))
							# winner = choice(users)
							# await channel.send(f"Congratulations {winner.mention} on winning the Giveaway")

	"""
def setup(bot):
    bot.add_cog(giveaways(bot))