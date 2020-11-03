import discord
import json
import random
#wasi if you see this ima get a bluefoxhosting server for #the bot i will make it under an account i will give you #access to
from  discord.ext import commands


bot = commands.Bot(command_prefix=["=",";",","])
TOKEN = ""

class Account():
	def __init__(self, data):
		self.wallet = data["wallet"]
		self.bank = data["bank"]
		self.inventory = data["inventory"]
		self.total = data["wallet"] + data["bank"]

shop_items = {
	"Banana": 100,
	"Apple": 200,
	"Mango": 300,
        "Dildo": 500,
        "Phone": 10000,
        "Gaming Computer": 100000
}
jobs = [
                        "Macdonalds",
                        "Walmart",
                        "Microsoft",
                        "Burger king",
                        "Karen"
                ]
job = random.choice(jobs)
if __name__ == "__main__":
	with open("data.json") as f:
		bot.data = json.load(f)

def refresh_data():
	with open("data.json") as f:
		bot.data = json.load(f)

def get_account(user: discord.User):
	refresh_data()
	return Account(bot.data[str(user.id)])

def save_data():
	with open("data.json", "w") as f:
		json.dump(bot.data, f, indent=4)

def make_account(user: discord.User):
	refresh_data()
	bot.data[user.id] = {
		"wallet": 0,
		"bank": 0,
		"inventory": [],
	}
	save_data()


@bot.event
async def on_ready():
        print("BOT IS READY")

@bot.command()
async def owner(ctx):
	    # Please keep this the way it is, thanks :)
        await ctx.send("Bot made by `Wasi Master#6969` and **owned**/maintained by `yt_ygrunn1ngark456#1144`")
        
@bot.command(aliases=["bal"])
async def balance(ctx, user: discord.User = None):
	user = user or ctx.author
	if not bot.data.get(str(user.id), False):
		# User does not have a account
		make_account(user)
	account = get_account(user)
	embed = discord.Embed(
		title=user.name,
		description=(
			f"Wallet: {account.wallet}\n"
			f"Bank : {account.bank}\n"
			f"Total : {account.total}\n"
			),
		color=discord.Colour.green()
	)
	await ctx.send(embed=embed)

@bot.command(aliases=["with"])
async def withdraw(ctx, amount):
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
		make_account(ctx.author)
	account = get_account(ctx.author)
	shortcuts = ["all", "half", "quarter"]
	if amount in shortcuts:
		if shortcuts.index(amount) == 0:
			amount = account.bank
		elif shortcuts.index(amount) == 1:
			amount = round(account.bank / 2)
		elif shortcuts.index(amount) == 2:
			amount = round(account.bank / 4)
	else:
		try:
			amount = int(amount)
		except Exception:
			return await ctx.send("Invalid amount")
	if account.bank < amount:
		return await ctx.send("You don't have that much money in your bank")
	bot.data[str(ctx.author.id)]["bank"] = account.bank - amount
	bot.data[str(ctx.author.id)]["wallet"] = account.wallet + amount
	save_data()
	await ctx.send(f"Succesfully withdrawn {amount} coins :coin:")

@bot.command(aliases=["dep"])
async def deposit(ctx, amount):
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
		make_account(ctx.author)
	account = get_account(ctx.author)
	shortcuts = ["all", "half", "quarter"]
	if amount in shortcuts:
		if shortcuts.index(amount) == 0:
			amount = account.wallet
		elif shortcuts.index(amount) == 1:
			amount = round(account.wallet / 2)
		elif shortcuts.index(amount) == 2:
			amount = round(account.wallet / 4)
	else:
		try:
			amount = int(amount)
		except Exception:
			return await ctx.send("Invalid amount")
	
	if account.wallet < amount:
		print(f"{account.wallet} < {amount}")
		return await ctx.send("You don't have that much money in your wallet")
	bot.data[str(ctx.author.id)]["wallet"] = account.wallet - amount
	bot.data[str(ctx.author.id)]["bank"]   = account.bank   + amount
	save_data()
	await ctx.send(f"Succesfully deposited {amount} coins :coin:")


@bot.command(aliases=["inv"])
async def inventory(ctx, user: discord.User = None):
	user = user or ctx.author
	if not bot.data.get(str(user.id), False):
		# User does not have a account
		make_account(user)
	account = get_account(user)
	embed = discord.Embed(
		title=user.name,
		description=", ".join(account.inventory) if account.inventory else "No items in your inventory :(",
		color=discord.Colour.green()
	)
	await ctx.send(embed=embed)
  
@bot.command()
async def shop(ctx):
	embed = discord.Embed(
		title='Shop',
		description="\n".join(f"{name} - {price} coins :coin:" for name, price in shop_items.items()),
		color=discord.Colour.green()
	)
	await ctx.send(embed=embed)

@bot.command()
async def buy(ctx, item):
	item = item.lower()
	if not item in shop_items:
		return await ctx.send("Item not available in the shop")
	coins = shop_items[item]
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
		make_account(ctx.author)
	ac = get_account(ctx.author)
	if ac.wallet < coins:
		return await ctx.send("Insufficient Coins")
	bot.data[str(ctx.author.id)]["wallet"] = ac.wallet - coins
	ac.inventory.append(item)
	bot.data[str(ctx.author.id)]["inventory"] = ac.inventory
	save_data()
	await ctx.send(f"Succesfully brought {item} for {coins} coins :coin:")

@bot.command()
async def sell(ctx, item):
	item = item.lower()
	if not item in shop_items:
		return await ctx.send("Item not valid")
	coins = round(shop_items[item] * 0.8)
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
		make_account(ctx.author)
	ac = get_account(ctx.author)
	try:
			index = ac.inventory.index(item)
			del ac.inventory[index]
	except ValueError:
		await ctx.send("You don't have that item")
	bot.data[str(ctx.author.id)]["wallet"] = ac.wallet + coins
	bot.data[str(ctx.author.id)]["inventory"] = ac.inventory
	save_data()
	await ctx.send(f"Succesfully sold {item} for {coins} coins :coin:")

@bot.command()
async def refresh(ctx):
	refresh_data()

@bot.command()
async def beg(ctx):
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
		make_account(ctx.author)
	account = get_account(ctx.author)
	amount = random.randint(100, 500)
	bot.data[str(ctx.author.id)]["wallet"] = account.wallet + amount
	save_data()
	await ctx.send(f"Someone gave you {amount} coins :coin:")
@bot.command()
async def work(ctx):
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
	 make_account(ctx.author)
	account = get_account(ctx.author)
	amount = random.randint(500, 5000)
	bot.data[str(ctx.author.id)]["wallet"] = account.wallet + amount
	save_data()
       
	await ctx.send(f"worksed as {job} and got {amount} coins :coin:")

@bot.command()
async def steal(ctx, person: discord.Member):
	if not bot.data.get(str(ctx.author.id), False):
		# User does not have a account
		make_account(ctx.author)
	if not bot.data.get(str(person.id), False):
		# Person does not have a account
		make_account(person)
	user_account = get_account(ctx.author)
	other_account = get_account(person)
	if other_account.wallet < 1:
		return await ctx.send(f"{person} has no money to steal :(")
	if other_account.wallet < 500:
		return await ctx.send(f"{person} has less than 500 coins so can't steal :(")
	amount = random.randint(100, 500)
	bot.data[str(ctx.author.id)]["wallet"] = user_account.wallet + amount
	bot.data[str(person.id)]    ["wallet"] = other_account.wallet - amount
	save_data()
	await ctx.send(f"You stole {amount} coins :coin: from {person.name}")

bot.run(TOKEN)