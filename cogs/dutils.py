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
from library.constants import Emotes
from main import is_staff

class dutils(commands.Cog, name='dutils'):
	def __init__(self, bot):
		self.bot = bot
	@commands.command()
	@commands.check(is_staff)
	async def heist(self,ctx,timez,amount):
		await ctx.message.delete()
		wa = self.bot.get_emoji(Emotes.w_arrow)
		pa = self.bot.get_emoji(Emotes.p_arrow)
		ping = ctx.guild.get_role(824654448944873552)
		await ctx.send(ping.mention)
		embed = discord.Embed(title=":money_with_wings: Heist Time!! :money_with_wings:",description=f"{pa} **Heist Details**\n{wa} Amount - {amount}\n{wa} Time - {timez}\n{pa} **Things To Remember:**\n{wa}Type `join heist` after channel is unlocked\n{wa} Remember to withdraw `2000` before heist\n{wa} Use a life saver before heist\n{wa} We will not remove the slowmode anytime during the heist",color=ctx.author.color)
		await ctx.send(embed=embed)

def setup(bot):
	bot.add_cog(dutils(bot))