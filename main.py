import discord, timeago, requests, datetime,random, json, time, os, urbandict
from os import listdir
from library import constants, funcs
from discord.ext import commands
from colorthief import ColorThief
import keep_alive
from discord.utils import get
from discord_buttons_plugin import *
import asyncio
from discord.ext.tasks import loop
with open("data/gawinit.json","r") as m:
	gawinit = json.load(m)
gawinit["status"] = 0
with open("data/gawinit.json","w") as z:
	json.dump(gawinit,z)

bot = commands.Bot(command_prefix = constants.Config.PREFIX, intents=discord.Intents.all())
buttons = ButtonsClient(bot)
bot.cur = constants.Config.CURRENCY_ICON
bot.color = constants.Config.COLOR_THEME
currencyname = constants.Config.CURRENCY_NAME
TOKEN = constants.Config.BOT_TOKEN
class HierarchyError(commands.CommandError):
    def __init__(self, message="Role hierarchy wrong."):
        self.message = message
        super().__init__(self.message)
        

async def is_botdev(ctx):
	roles = [ctx.author.top_role.id, ctx.author.roles[-2].id, ctx.author.roles[-3].id]
	if roles[0] in constants.Roles.BOTMODS or roles[1] in constants.Roles.BOTMODS or roles[2] in constants.Roles.BOTMODS or ctx.author.id in constants.Roles.BOTMODS:
		return True
	else:
		return False
async def is_staff(ctx):
	role = discord.utils.find(lambda r: r.id == constants.Roles.STAFF, ctx.message.guild.roles)
	if role in ctx.author.roles:
		return True
	else:
		return False
async def is_not_blacklisted(ctx):
	funcs.open_bl(ctx.author)
	users = funcs.get_bl_data()
	user = ctx.author
	if users[str(user.id)]["blacked"]:
		return False
	else:
		return True
@loop()
async def gaw_utils(ctx):
	with open("data/gaw.json","r") as f:
		gaw = json.load(f)
	for item in gaw:
		if item["time"] == 0:
			return
		new_msg = await ctx.channel.fetch_message(int(item))
		await new_msg.edit(content="hi")
		
@loop(seconds=10)
async def change_status():
	await asyncio.sleep(8)
	mode = ["playing","listening","watching"]
	statuses = ["Doggo Dankers","Niraj swearing","Levi be Catfishing","Ace spamming lines of code","Oh my Eris what are you doing","Hi I'm Joe, I sell dildos","dd?help","Percy likes dogs do you?","Made by Ace and Eris","#DoggoDankers","Bark Bark Bark","Why What When Why How","dog.exe has started",f"Would you like some doggocoins?","Levi be cute","Eris == Kaneki","Bow down humans","Well hello there","Why are you looking at this?","Living legend"]
	modal = random.choice(mode)
	status = random.choice(statuses)
	if modal == "watching":
		await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{status}"))
	if modal == "listening":
		await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.listening, name=f"{status}"))
	if modal == "playing":
		await bot.change_presence(status = discord.Status.do_not_disturb, activity=discord.Activity(type=discord.ActivityType.playing, name=f"{status}"))

@bot.event
async def on_ready():
	print('Ready!')
	bot.loop.create_task(change_status())

bot.remove_command("help")

@bot.command(name="help")
@commands.check(is_not_blacklisted)
async def help(ctx):
	embed = (discord.Embed(title='DoggoBot', description = "**DoggoCoins can be earned by:**\n1. Bumping the server in <#824641127315406888>\n2. Through commands like `=beg` and `=daily`\n3. Voting for us on Top.gg\n4. Boosting the Server\n5. Investing in Us.\n\n**DoggoCoins can be used for:**\n1. Trading into DMC\n2. For awesome server perks like extra claimtime, private rooms, etc.\nUse `=shop` to know more.", color = bot.color)
	.set_footer(text="While frowned upon you can do anything with these coins such as bet or giveaways"))
	await ctx.send(embed=embed)
@bot.command()
@commands.check(is_not_blacklisted)
async def donations(ctx,user:discord.Member=None):
	if user == None:
		user = ctx.author
	await funcs.open_donation(user)
	users = funcs.load_donation()
	amount = users[str(user.id)]["donations"]
	embed = discord.Embed(title=f"{user.name}'s donations",description = f"**Amount Donated:** `{amount}`",color=user.color)
	await ctx.send(embed=embed)
@bot.command(aliases=["donationadd"])
@commands.check(is_not_blacklisted)
async def dadd(ctx,user:discord.Member,amount:int):
	await funcs.open_donation(user)
	users = funcs.load_donation()
	users[str(user.id)]["donations"] += amount
	with open("data/donations.json","w") as d:
		json.dump(users,d)
	await ctx.send(f"Successfully added {amount} to {user.name}'s donations")
@bot.command(aliases=["donationremove"])
@commands.check(is_not_blacklisted)
async def drm(ctx,user:discord.Member,amount:int):
	await funcs.open_donation(user)
	users = funcs.load_donation()
	users[str(user.id)]["donations"] -= amount
	with open("data/donations.json","w") as d:
		json.dump(users,d)
	await ctx.send(f"Successfully minused {amount} from {user.name}'s donations")
@bot.command(name='user', aliases=['self', 'userstats'])
@commands.check(is_not_blacklisted)
async def user(ctx, user:discord.Member=None):
	if not user:
		user=ctx.author
	url = user.avatar_url
	funcs.open_user(user)
	users = funcs.get_users_data()
	amount = users[str(user.id)]["coins"]
	r = requests.get(url, allow_redirects=True)
	open('tempimg.gif', 'wb').write(r.content)
	color_thief = ColorThief('tempimg.gif')
	# get the dominant color
	dominant_color = color_thief.get_color(quality=1)
	created_at = user.created_at.strftime('%-d %b %Y')
	joined_at = user.joined_at.strftime('%-d %b %Y')
	now = datetime.datetime.now() + datetime.timedelta(seconds = 60 * 3.4)
	main = str(dominant_color).replace('(','').replace(')','').split(", ")
	x = int(main[0])
	y = int(main[1])
	z = int(main[2])

	badges = []
	if r.headers.get('content-type') == "image/gif":
		badges.append("<:nitro:847058195037028382>")
	if user.public_flags.hypesquad_bravery:
		badges.append("<:hypesquad_balance:847052433250713620>")
	if user.public_flags.hypesquad_balance:
		badges.append("<:hypesquad_bravery:847052433116495872>")
	if user.public_flags.hypesquad_brilliance:
		badges.append("<:hypesquad_brilliance:847052433708285963>")
	cretimeago = timeago.format(user.created_at, now)
	jointimeago = timeago.format(user.joined_at, now)
	final1 = str(badges).replace("]","").replace("[","").replace(",","  ").replace("'", "")
	embed = discord.Embed(title=user.name, description = f'{final1}\n\n**Joined Discord on:** {created_at} ({cretimeago})\n**Joined {ctx.guild.name} on:** {joined_at} ({jointimeago})', colour = discord.Color.from_rgb(x,y,z))
	embed.add_field(name='Bot Related UserInfo', value = f"**{currencyname}** {amount} {bot.cur}")
	embed.timestamp = datetime.datetime.utcnow()
	embed.set_thumbnail(url=user.avatar_url)
	await ctx.send(embed=embed)

@bot.command(name='buttons')
@commands.check(is_botdev)
async def _buttons(ctx):
	await buttons.send(
	content = "This is an example message!", 
	channel = ctx.channel.id,
	components = [
		ActionRow([
			Button(
				label="Hello", 
				style=ButtonType().Primary, 
				custom_id="button_one"       
			)
		])
	]
	)

@buttons.click
async def button_one(ctx):
	await ctx.reply('Hello Clicker!')

@bot.command(name='define', aliases = ['lookup', 'urban'])
@commands.check(is_not_blacklisted)
async def _define(ctx, to_define:str=None):
	if not to_define:
		return await ctx.send('What should I define???')

	url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

	querystring = {"term":to_define}

	headers = {
		'x-rapidapi-key': "5be05ffb96mshfe7579bba5baf5ap1b6240jsnad885dc354f3",
		'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com"
		}

	response = requests.request("GET", url, headers=headers, params=querystring)
	main = response.json()["list"][0]
	word = main["word"]
	definition = main["definition"]
	example = main["example"]
	url = main["permalink"]
	auth = main["author"]
	up = main["thumbs_up"]
	down = main["thumbs_down"]
	embed = discord.Embed(title=f"Definition of {word}",url=url, description = definition, colour = bot.color)
	embed.add_field(name='Example', value = example, inline=False)
	embed.add_field(name='** **', value=f"{up} 👍\n\n{down} 👎")
	embed.set_footer(text=f"Requested by {ctx.author.name} | Sent by {auth}", icon_url=ctx.author.avatar_url)
	embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/847409923166830612/847853404999254056/Urban-Dictionary.png")
	embed.timestamp = datetime.datetime.utcnow()
	await ctx.send(embed=embed)

@bot.command(name='bal', aliases = ['balance'])
@commands.check(is_not_blacklisted)
async def _bal(ctx, user:discord.Member=None):
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()
	if not user:
		user = ctx.author
	funcs.open_user(user)
	users = funcs.get_users_data()
	bal = users[str(user.id)]["coins"]
	embed = discord.Embed(title=f"{user.name}'s Points", description = f"**{currencyname}** {bal} {bot.cur}", color = bot.color)
	await ctx.send(embed=embed)

@bot.command(name='beg')
@commands.cooldown(1,30, commands.BucketType.user)
@commands.check(is_not_blacklisted)
async def _beg(ctx):
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()
	user= ctx.author
	msgs = ["Humans have become cheaper than us, dogs", "Unable to Translate (too many swears)", "Ew Gross Human, here take some", "Humans dominated us for ages. Now they are begging from us. That's Karma."]
	msg = random.choice(msgs)
	amount = random.randrange(0,10)
	embed= discord.Embed(title="Bark Bark Bark, Barkk", description = f"**Translation:** {msg}\nThe doggo gave you {amount} coins.", color = bot.color)
	await ctx.send(embed=embed)
	funcs.open_user(user)
	users = funcs.get_users_data()
	users[str(user.id)]["coins"] += amount
	with open('data/bank.json','w') as f:
		json.dump(users,f)

@bot.command(name='drop')
@commands.check(is_botdev)
@commands.check(is_not_blacklisted)
async def _drop(ctx, amount:int):
	await ctx.message.delete()
	types = ['msg', 'react']
	type = random.choice(types)
	if type == 'msg':
		msgs = ["percy sux", "levi sux", "make me admin"]
		msg1 = random.choice(msgs)
		embed = discord.Embed(title = f'{currencyname} Drop!', description = f'Type `{msg1}` to get {amount} {currencyname}!', colour = bot.color)
		await ctx.send(embed=embed)
		def check(msg):
			return msg.content == msg1
		msg = await bot.wait_for('message', check=check, timeout=30)
		await ctx.send(f"{msg.author.mention} Just got {amount} {currencyname}! GG!\nYou can trade these in for DMC (coming soon)")
		funcs.open_user(msg.author)
		users = funcs.get_users_data()
		users[str(msg.author.id)]["coins"] += amount
		with open('data/bank.json','w') as f:
			json.dump(users,f)
	elif type == 'react':
		embed = discord.Embed(title = f'{currencyname} Drop!', description = f'React to get {amount} {currencyname}!', colour = bot.color)
		main=await ctx.send(embed=embed)
		await main.add_reaction("<a:Winkles_1:824695592194015245>")
		def check(msg, user):
			return user.bot != True
		msg, user = await bot.wait_for('reaction_add', check=check, timeout=30)
		await ctx.send(f"{user.mention} Just got {amount} {currencyname}! GG!\nYou can trade these in for DMC (coming soon)")
		funcs.open_user(user)
		users = funcs.get_users_data()
		users[str(user.id)]["coins"] += amount
		with open('data/bank.json','w') as f:
			json.dump(users,f)

@bot.command(aliases=["inv"])
@commands.check(is_not_blacklisted)
async def bag(ctx,member:discord.Member=None):
		funcs.open_user(ctx.author)
		user = ctx.author
		users = funcs.get_users_data()

		try:
			items = users[str(user.id)]["items"]
		except:
			items = []


		em = discord.Embed(title = "items",color=bot.color)
		for item in items:
			name = item["item"]
			em.add_field(name = name, value = None, inline = False)
		await ctx.send(embed = em)

@bot.command()
@commands.check(is_not_blacklisted)
async def use(ctx,item):
	funcs.open_user(ctx.author)
	users1 = funcs.get_rooms_data()
	user = ctx.author
	try:
		roomid = users1[str(user.id)]["roomid"]
		stats= False
	except KeyError:
		roomid = None
		stats = True
	if roomid != None and stats == False:
		return await ctx.send(f'You already have a room: <#{users1[str(user.id)]["roomid"]}>')
	users = funcs.get_users_data()
	if item == "prp":
		try:
			items = users[str(user.id)]["items"]
		except:
			items = []
		for itemx in items:
			print(itemx)
			if item not in itemx["item"]:
				return await ctx.send("You do not have a Private room pass")
		category = discord.utils.get(ctx.guild.categories, name='Private VC\'s')
		vc = await ctx.guild.create_voice_channel(str(ctx.author), category=category)
		overwrite = vc.overwrites_for(ctx.guild.default_role)
		overwrite.view_channel = False
		await vc.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		overwrite = vc.overwrites_for(ctx.author)
		overwrite.view_channel = True
		overwrite.connect = True
		await vc.set_permissions(ctx.author, overwrite=overwrite)
		inv=await vc.create_invite()
		embed = discord.Embed(title='Private Room Created', description = f"**Join Channel:** [{vc.name}]({inv})\n**Duration:** 1 hour", color = bot.color)
		funcs.open_room(ctx.author, vc.id, vc.name)
		users1 = funcs.get_rooms_data()
		users1[str(user.id)]["roomid"] = vc.id
		with open('data/rooms.json','w') as f:
			json.dump(users1,f)
		users = funcs.get_rooms_data()
		await ctx.send(embed=embed)
		await asyncio.sleep(3600)
		await vc.delete()
		users[str(user.id)]["roomid"] = None
		users[str(user.id)]["users"] = []
		with open('data/rooms.json','w') as f:
			json.dump(users,f)
		return

@bot.command(name='room')
@commands.check(is_not_blacklisted)
async def room(ctx, action:str, user1:discord.Member=None):
	users = funcs.get_rooms_data()
	user = ctx.author
	try:
		roomid = users[str(user.id)]["roomid"]
		if roomid == None:
			return await ctx.send('You do not have a private room created.')
	except KeyError:
		return await ctx.send('You do not have a private room created.')
	vc = ctx.guild.get_channel(roomid)
	if action == 'add':
		overwrite = vc.overwrites_for(user1)
		overwrite.view_channel = True
		overwrite.connect = True
		await vc.set_permissions(user1, overwrite=overwrite)
		users[str(user.id)]["users"].append(user1.id)
		with open('data/rooms.json','w') as f:
			json.dump(users,f)
		return await ctx.send(f'Added {user1.mention}. They can now access your Private Room: {vc.name}')
	elif action == 'remove':
		overwrite = vc.overwrites_for(user1)
		overwrite.view_channel = False
		overwrite.connect = False
		await vc.set_permissions(user1, overwrite=overwrite)
		users[str(user.id)]["users"].remove(user1.id)
		with open('data/rooms.json','w') as f:
			json.dump(users,f)
		return await ctx.send(f'Removed {user1.mention}\'s access to Private Room: {vc.name}')
	elif action == 'delete':
		await vc.delete()
		users[str(user.id)]["roomid"] = None
		users[str(user.id)]["users"] = []
		with open('data/rooms.json','w') as f:
			json.dump(users,f)
		return await ctx.send(f'Deleted your Private Room: {vc.name}')
	elif action == 'users':
		roomusers = users[str(user.id)]["users"]
		roomusersfinal = ""
		for user in roomusers:
			user = bot.get_user(user)
			roomusersfinal += f"{user.mention}\n"
		embed = discord.Embed(title=f'{vc.name}\'s Users', description = roomusersfinal, color = bot.color)
		await ctx.send(embed=embed)

	
@bot.command(name='shop', aliases = ['store'])
@commands.check(is_not_blacklisted)
async def _shop(ctx, categ=None):
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()

	if categ == None:
		embed = discord.Embed(title='DoggoShop', color = bot.color)
		embed.add_field(name='Dank Memer Trading (Not against TOS)', value = f'Use `=shop dmc`', inline=False)
		embed.add_field(name='Server Perks', value = 'Cool Server Perks like DJ role, private rooms, etc.\n`=shop roles`')
		embed.set_footer(text = "Use `=buy [id]` to buy! (coming soon)")
		await ctx.send(embed=embed)
	
	elif categ == 'dmc':
		embed = discord.Embed(title='DoggoShop | DMC', color = bot.color)
		embed.add_field(name='Dank Memer Coins', value = f'**Price:** 100 DMC for 1 {bot.cur}', inline=False)
		embed.add_field(name='Dank Memer Items', value = f'**Rare Pepe:** `650` {bot.cur}\nID:`rare`\n**Pepe Coin:** `5,500` {bot.cur}\nID:`pepec`\n**Pepe Medal:** `90,000` {bot.cur}\nID: `pepem`')
		embed.set_footer(text = "Use `=buy [id]` to buy! (coming soon)")
		await ctx.send(embed=embed)

	elif categ == 'roles':
		embed = discord.Embed(title='DoggoShop | Server Perks', color = bot.color)
		embed.add_field(name='Private Room Pass', value = f'**Price:** ~~1000~~ 600 [40% OFF] {bot.cur}\n**ID:** `prp`\nCreate a Private VC whenever you want to, free of charge', inline=False)
		embed.add_field(name='Create Private Room (one-time)', value = f'**Price:** 100 {bot.cur}\n**ID:** `room`\nCreate Private VC one-time', inline=False)
		embed.add_field(name='@DJ Role', value = f'Control Music throughout the server.\n**Price:** 69 {bot.cur}\nID: `dj`')
		embed.set_footer(text = "Use `=buy [id]` to buy! (coming soon)")
		await ctx.send(embed=embed)

@bot.command(name='math')
@commands.check(is_not_blacklisted)
async def math(ctx, *, to_math):
	to_math = to_math.replace('m', '000000').replace('k', '000')
	final = eval(to_math)
	await ctx.send(f"**Calculated:** `{final}`")

@bot.command(name='buy')
@commands.check(is_not_blacklisted)
async def _buy(ctx, item:str, amount:int=1):
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()
	funcs.open_user(ctx.author)
	users = funcs.get_users_data()
	user = ctx.author
	if item == "dmc" or item == "pepec" or item == "pepe" or item == "rare":
		price = amount/100
		if item == "pepec":
			price = 5500
		if item == "pepe" or item == "rare":
			price = 650
		if users[str(user.id)]["coins"] < price:
			return await ctx.send('You don\'t have enough DoggoCoins.')
		if await funcs.conf(bot, ctx, f"buy {amount} {item} for {price} {bot.cur}"):
			users[str(user.id)]["coins"] -= amount
			await ctx.send('Successfully placed your order.\nYour order will reach you within 24 hours.')
			channel = ctx.guild.get_channel(847406862680719360)
			await channel.send(f"<@&847407041169195010>, **New Order!**\n{ctx.author.mention} just ordered {amount} **{item}**!\nPay them ASAP")
			with open('data/bank.json','w') as f:
				json.dump(users,f)
	elif item == "prp":
		price = 600
		if users[str(ctx.author.id)]["coins"] < price:
			return await ctx.send('You don\'t have enough DoggoCoins.')
		if await funcs.conf(bot, ctx, f"buy A private room pass for {price} {bot.cur}"):
			obj = {"item":item}				
			users[str(ctx.author.id)]["items"] = [obj]        
			users[str(user.id)]["coins"] -= price
			with open("data/bank.json","w") as f:
				json.dump(users,f)
			await ctx.send("You bought a Private Room Pass!")
			return
	elif item == 'room':
		users1 = funcs.get_rooms_data()
		user = ctx.author
		try:
			roomid = users1[str(user.id)]["roomid"]
			stats= False
		except KeyError:
			roomid = None
			stats = True
		if roomid != None and stats == False:
			return await ctx.send(f'You already have a room: <#{users1[str(user.id)]["roomid"]}>')
		price = 100
		if users[str(ctx.author.id)]["coins"] < price:
			return await ctx.send('You don\'t have enough DoggoCoins.')
		if await funcs.conf(bot, ctx, f"buy A temporary room for {price} {bot.cur}"):        
			users[str(user.id)]["coins"] -= price
			with open("data/bank.json","w") as f:
				json.dump(users,f)
		funcs.open_user(ctx.author)
		users = funcs.get_users_data()
		category = discord.utils.get(ctx.guild.categories, name='Private VC\'s')
		vc = await ctx.guild.create_voice_channel(str(ctx.author), category=category)
		overwrite = vc.overwrites_for(ctx.guild.default_role)
		overwrite.view_channel = False
		await vc.set_permissions(ctx.guild.default_role, overwrite=overwrite)
		overwrite = vc.overwrites_for(ctx.author)
		overwrite.view_channel = True
		overwrite.connect = True
		await vc.set_permissions(ctx.author, overwrite=overwrite)
		inv=await vc.create_invite()
		embed = discord.Embed(title='Private Room Created', description = f"**Join Channel:** [{vc.name}]({inv})\n**Duration:** 1 hour", color = bot.color)
		funcs.open_room(ctx.author, vc.id, vc.name)
		users1 = funcs.get_rooms_data()
		users1[str(user.id)]["roomid"] = vc.id
		with open('data/rooms.json','w') as f:
			json.dump(users1,f)
		users = funcs.get_rooms_data()
		await ctx.send(embed=embed)
		await asyncio.sleep(3600)
		await vc.delete()
		users[str(user.id)]["roomid"] = None
		users[str(user.id)]["users"] = []
		with open('data/rooms.json','w') as f:
			json.dump(users,f)

	elif item == 'dj':
		funcs.open_user(ctx.author)
		users = funcs.get_users_data()
		price = 69
		if users[str(ctx.author.id)]["coins"] < price:
			return await ctx.send('You don\'t have enough DoggoCoins.')
		if await funcs.conf(bot, ctx, f"buy the DJ Role for {price} {bot.cur}"):        
			users[str(user.id)]["coins"] -= price
			with open("data/bank.json","w") as f:
				json.dump(users,f)
			dj = discord.utils.get(ctx.guild.roles, id=824848049259282443)
			await ctx.author.add_roles(dj)
			await ctx.send(f'Added {dj.name} to your roles.')


				
@bot.command(name='gmtu', aliases = ['givemoney'])
@commands.check(is_staff)
@commands.check(is_not_blacklisted)
async def _gmtu(ctx, user:discord.Member, amount:int):
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()
	users = funcs.get_users_data()
	users[str(user.id)]["coins"] += amount
	with open('data/bank.json','w') as f:
		json.dump(users,f)
	await ctx.send(f'Added {amount} {bot.cur} to {user.name}\'s Points.')

@bot.command(name="daily")
@commands.check(is_not_blacklisted)
@commands.cooldown(1,86400, commands.BucketType.user)
async def _daily(ctx):
	funcs.open_user(ctx.author)
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()
	embed = discord.Embed(title="Daily",description=f"What did the dog say?\n The dog said have 10 {bot.cur}",color=bot.color)
	users = funcs.get_users_data()
	users[str(ctx.author.id)]["coins"] += 10
	with open("data/bank.json","w") as f:
		json.dump(users,f)
	await ctx.send(embed=embed)

@bot.command(name='give',aliases=["share"])
@commands.check(is_not_blacklisted)
async def give(ctx,user,amount:int):
	await funcs.open_user(ctx.author)
	if not constants.Getters.get_usage_status(ctx):
		msg = await ctx.send('you cannot use commands here, use it in <#847409923166830612>.')
		await asyncio.sleep(5)
		return await msg.delete()
	inte = "null"
	try:
		user = int(user)
	except:
		inte = False
		await ctx.send(f"Please give {bot.cur} through ids")
	users = funcs.get_users_data()
	if users[str(ctx.author.id)]["coins"] < amount:
		await ctx.send("Not enough points")
		return
	else:
		if inte == False:
			users[str(ctx.author.id)]["coins"] -= amount
			users[str(user.id)]["coins"] += amount
			funcs.pdump(users)
			await ctx.send("Finished transfer")
		else:
			users[str(ctx.author.id)]["coins"] -= amount
			users[str(user)]["coins"] += amount
			funcs.pdump(users)
			await ctx.send("Finished transfer")
"""
@bot.command(name='ban', aliases = ('b',))
@commands.has_permissions(ban_members=True)
async def _ban(ctx, user:discord.Member, *, reason=None):
	if ctx.author.top_role.position < user.top_role.position:
		raise errors.HierarchyError()
	await ctx.guild.ban(user, reason=reason)
	return await ctx.send(f'**Banned {user.name}**\n**Reason:** {reason}')

@bot.command(name='kick', aliases = ('k',))
@commands.has_permissions(kick_members=True)
async def _kick(ctx, user:discord.Member, *, reason=None):
	if ctx.author.top_role.position < user.top_role.position:
		raise errors.HierarchyError()
	await ctx.guild.ban(user, reason=reason)
	return await ctx.send(f'**Kicked** {user.name}\n**Reason:** {reason}')

@bot.command(name='mute', aliases = ['m'])
@commands.check(is_botdev)
async def _mute(ctx, user:discord.Member, *,reason=None):
	muterole = discord.utils.get(ctx.guild.roles, id=constants.Roles.MUTEROLE)
	await user.add_roles(muterole)
	return await ctx.send(f'Muted {user.name}')

@bot.command(name='unmute', aliases = ['um'])
@commands.check(is_botdev)
async def _unmute(ctx, user:discord.Member, *,reason=None):
	muterole = discord.utils.get(ctx.guild.roles, id=constants.Roles.MUTEROLE)
	await user.remove_roles(muterole)
	return await ctx.send(f'Unmuted {user.name}')

@bot.command(name='hardmute', aliases = ['hm'])
@commands.check(is_botdev)
async def _hardmute(ctx, user:discord.Member, *, time:int=None):
	if not time:
		time = 10
	muterole = discord.utils.get(ctx.guild.roles, id=constants.Roles.MUTEROLE)
	userroles = []
	for role in user.roles[1:]:
		if str(role.name) == '@everyone' or 'everyone' in role.name:
			pass
		try:
			await user.remove_roles(role)
			userroles.append(role)
		except:
			pass
		await asyncio.sleep(1)
	await user.add_roles(muterole)
	await ctx.send(f'Hardmuted {user.name} for {time} seconds.')
	await asyncio.sleep(time)
	await user.remove_roles(muterole)
	for role in userroles:
		await user.add_roles(role)
		await asyncio.sleep(1)
"""
@bot.command(name='setbal', aliases = ['sb'])
@commands.check(is_not_blacklisted)
@commands.check(is_botdev)
async def sb(ctx, user:discord.Member, amount:int):
	users = funcs.get_users_data()
	users[str(user.id)]["coins"] = amount
	funcs.pdump(users)
	await ctx.send(f'Set {amount} to {user.name}\'s Points.')

@bot.command(name='commands')
async def _commands(ctx):
	final = ""
	for command in bot.commands:
		final += f"{command.name}\n"
	await ctx.send(f'**__My Commands__**\n{final}')

@bot.command(name='selfrole', alises = ['niraj'])
async def niraj(ctx):
	if ctx.author.id != 775198018441838642 and ctx.author.id != 746904488396324864:
		return
	role = discord.utils.get(ctx.guild.roles, id=824626266094305331)
	await ctx.author.add_roles(role)
	await ctx.send('<@579905582778155008> i added niraj role to ace dont ban pls lol')

@commands.command(name="src", aliases = ['source'])
@commands.check(is_not_blacklisted)
async def _src(ctx):
	embed = discord.Embed(title='Source Code', description = '[Go to GitHub](https://github.com/Ace-9999/Akaza)', color = bot.color)
	embed.set_footer(text="open source project")
	await ctx.send(embed=embed)

@bot.command(name='blacklist', aliases = ['bl'])
async def blacklist(ctx, user:discord.Member):
	if ctx.author.id not in constants.Roles.DEVS:
		return
	funcs.open_bl(user)
	users= funcs.get_bl_data()
	if users[str(user.id)]["blacked"]:
		return await ctx.send('Already Blacklisted.')
	users[str(user.id)]["blacked"] = True
	with open('data/bl.json','w') as f:
		json.dump(users,f)
	await ctx.send(f'Blacklisted {user.mention}')

@bot.command(name='unblacklist', aliases = ['ubl'])
async def unblacklist(ctx, user:discord.Member):
	if ctx.author.id not in constants.Roles.DEVS:
		return
	funcs.open_bl(user)
	users= funcs.get_bl_data()
	if not users[str(user.id)]["blacked"]:
		return await ctx.send('Already Unblacklisted.')
	users[str(user.id)]["blacked"] = False
	with open('data/bl.json','w') as f:
		json.dump(users,f)
	await ctx.send(f'Unblacklisted {user.mention}')

@bot.command()
async def freezenick(ctx, user:discord.Member, *, nick):
	funcs.open_freeze(user)
	users = funcs.get_freezed_data()
	if users[str(user.id)]["freezed"]:
		return await ctx.send('Alr freezed.')
	funcs.start_freeze(user, nick)
	await user.edit(nick=nick)
	await ctx.send(f'Freezed {user.mention}\'s NickName')
@bot.command(aliases=["unfreezenick"])
async def ee(ctx,user:discord.Member):
	users = funcs.get_freezed_data()
	if str(user.id) not in users:
		await ctx.send("Never frozen")
		return
	del users[str(user.id)]
	with open("data/freezed.json","w") as z:
		json.dump(users,z)
	await ctx.send(f'Unfroze {user.mention}\'s NickName')
@bot.event
async def on_member_update(before, after):
	if before.nick != after.nick:
		user = before
		funcs.open_freeze(before)
		users = funcs.get_freezed_data()
		if users[str(user.id)]["freezed"]:
			oldnick = users[str(user.id)]["freezednick"]
			await user.edit(nick=oldnick)
		else:
			return

	
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandOnCooldown):
		return await ctx.send(error)
	elif isinstance(error, commands.MissingRequiredArgument):
		return await ctx.send(error)
	elif isinstance(error, commands.CommandNotFound):
		return await ctx.send(error)
	elif isinstance(error, commands.CheckFailure):
		return
	elif isinstance(error, asyncio.TimeoutError):
		return
	elif isinstance(error, HierarchyError):
		return await ctx.send('You can\'t do this action due to role hierarchy.')
	else:
		raise error
@bot.listen("on_message")
async def init_gaw(message):
	
	with open("data/gawinit.json","r") as f:
		ginit = json.load(f)
	if ginit["status"] == 1:
		return
	else:
		ginit["status"] += 1
		with open("data/gawinit.json","w") as a:
			json.dump(ginit,a)
		bot.loop.create_task(gaw_utils(message))
		gaw_utils.start(message)
		print("[Gaw_Utils]: Initialised")
@bot.listen("on_message")
async def boost_reward(message):
	funcs.open_user(message.author)
	if discord.MessageType ==  discord.MessageType.premium_guild_subscription:
		await message.channel.send(f"Thank you for boosting, enjoy 1000 {bot.cur}")

@bot.listen('on_message')
async def bump_reward(message):
	if message.channel.id != 824641127315406888:
		return # Ace do how many add points
	else:
		if message.author.id == 634866217764651009 and 'It\'s been 2 hours since the last successful bump, could someone run' in message.content:
			await message.channel.send(f'**Extra Reward:** 10 {bot.cur} to the first bumper.\nCan be traded for DMC!')
	funcs.open_user(message.author)
	if "!d bump" in message.content:
		def check(msg):
			return msg.author.bot == True
		msg = await bot.wait_for('message', check=check)
		if 'Please wait' in msg.content:
			await message.channel.send("Please wait for the timer to be over")
			return
		elif 'Bump done :thumbsup:' in msg.content:
			users = funcs.get_users_data()
			users[str(message.author.id)]["coins"] += 10
			with open('data/bank.json','w') as f:
				json.dump(users,f)
			await message.channel.send(f"Thank you for bumping, you have recieved 10 {bot.cur}")

bot.load_extension("jishaku")
for file in listdir('cogs/'):
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')
change_status.start()
keep_alive.keep_alive()
bot.run(TOKEN)