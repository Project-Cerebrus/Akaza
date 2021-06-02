import json, discord
from library import constants
def load_donation():
	with open("data/donations.json","r") as f:
		users = json.load(f)
	return users
async def open_donation(user):
	users = load_donation()
	if str(user.id) not in users:
		users[str(user.id)] = {}
		users[str(user.id)]["donations"] = 0
		with open("data/donations.json","w") as z:
			json.dump(users,z)
	else:
		return

def open_user(user):
	users = get_users_data()
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["coins"] = 0
		users[str(user.id)]["items"] = []

	with open('data/bank.json','w') as f:
		json.dump(users,f)

	return True
def get_users_data():
	with open('data/bank.json','r') as f:
		users = json.load(f)

	return users

def open_room(user, roomid, roomname=None):
	users = get_rooms_data()
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["roomid"] = roomid
		users[str(user.id)]["roomname"] = roomname
		users[str(user.id)]["users"] = []

	with open('data/rooms.json','w') as f:
		json.dump(users,f)

	return True
def get_rooms_data():
	with open('data/rooms.json','r') as f:
		users = json.load(f)

	return users

def open_bl(user):
	users = get_bl_data()
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["blacked"] = False

	with open('data/bl.json','w') as f:
		json.dump(users,f)

	return True
def get_bl_data():
	with open('data/bl.json','r') as f:
		users = json.load(f)

	return users

def open_freeze(user):
	users = get_freezed_data()
	if str(user.id) in users:
		return False
	else:
		users[str(user.id)] = {}
		users[str(user.id)]["freezed"] = False
		users[str(user.id)]["freezednick"]= None

	with open('data/freezed.json','w') as f:
		json.dump(users,f)

	return True

def get_freezed_data():
	with open('data/freezed.json','r') as f:
		users = json.load(f)

	return users

def start_freeze(user, nick):
	users = get_freezed_data()
	users[str(user.id)] = {}
	users[str(user.id)]["freezed"] = True
	users[str(user.id)]["freezednick"]= nick

	with open('data/freezed.json','w') as f:
		json.dump(users,f)

	return True

async def conf(bot,ctx, to_conf:str):
	msg = await ctx.send(f'Are you sure you want to {to_conf}?')
	await msg.add_reaction("👍")
	await msg.add_reaction("👎")
	def check(reaction, user):
		return user == ctx.author
	reaction, user = await bot.wait_for('reaction_add', check=check)
	await msg.remove_reaction(reaction,user)
	await msg.delete()
	if str(reaction) == "👍":
		await ctx.send(f"Successfully completeted {to_conf}")
		return True
	if str(reaction) == "👎":
		await ctx.send(f"Successfully stopped {to_conf}")
		return False

def pdump(users):
	with open("data/bank.json","w") as f:
		json.dump(users,f)

async def get_BOTMODS(ctx):
	BOTMODSROLES = []
	for role in constants.Roles.BOTMODS:
		final = await discord.utils.get(ctx.guild.roles, id=role)
		BOTMODSROLES.append(final.name)
	return BOTMODSROLES
	