import discord, os, dotenv, time, random, json
from discord.ext import commands
from economy import *
from functions import *
# Load environment variables from .env file
dotenv.load_dotenv()
TOKEN = os.getenv('token')
# Intents are required for certain events
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Set up the bot
bot = commands.Bot(command_prefix=".", intents=intents)
ec = Economy()

def save():
    file = open("save.json", "w")
    saveJson = {}
    for i in ec.accounts:
        saveJson[i.id] = ec.accounts[i].toJson()
    # print(saveJson)
    json.dump(saveJson, file)
    file.close()

def load():
    file = open("save.json", "r")
    jsonIN = json.load(file)
    # print(jsonIN)
    file.close()
    for i in jsonIN:
        userID = bot.get_user(int(i))
        ec.accounts[userID] = BankAccount(userID)
        ec.accounts[userID].loadJson(jsonIN[i])
    # print(ec.accounts)

async def sendEmbed(ctx, message:str, type:int = 0, usr:discord.Member = None):
    save()
    if usr == None: usr = ctx.author
    if type < 0: color = discord.Color.red()
    elif type > 0: color = discord.Color.green()
    else: color = discord.Color.blurple()
    embed = discord.Embed(color=color)
    embed.set_author(name=usr.display_name, icon_url=usr.display_avatar)
    embed.description = message
    await ctx.send(embed=embed)
    

@bot.event
async def on_ready():
    global ec
    await bot.change_presence(activity=discord.Activity(name="with your money", type=0))
    load()
    print(f'{bot.user} is now running')

@bot.command(brief="Returns Pong if the bot is online")
async def ping(ctx):
    await ctx.send('Pong!')
    
@bot.command(name="balance", aliases=["bal"], brief="Displays your balance. Use `.balance @<username>` to see the balance of someone else")
async def balance(ctx, target:discord.Member = None):
    if target == None: target = ctx.author
    usr = ec.getUser(target)
    msg = f"Cash: ${"{:,}".format(usr.cash)}\nBank: ${"{:,}".format(usr.balance)}\nTotal: ${"{:,}".format(usr.balance + usr.cash)}"
    await sendEmbed(ctx, msg, usr=target)
    
@bot.command(name="work", brief="Gives you a small amount of money. Has cooldown")
async def work(ctx):
    usr = ec.getUser(ctx.author)
    amount = random.randint(25, 750)
    usr.addMoney(amount)
    msg = functions.getWorkMsg(amount)
    await sendEmbed(ctx, msg, 1)
    
@bot.command(name="crime", brief="Gives you a large amount of money but there is a chance you lose money. Has cooldown")
async def crime(ctx):
    usr = ec.getUser(ctx.author)
    if bool(random.getrandbits(1)):
        amount = random.randint(1000, 5000)
        usr.addMoney(amount)
        msg = functions.getCrimeWin("{:,}".format(amount))
        await sendEmbed(ctx, msg, 1)
    else:
        amount = round((usr.cash+usr.balance) * random.uniform(0.25, 0.7))
        usr.cash -= amount
        msg = functions.getCrimeLose("{:,}".format(amount))
        await sendEmbed(ctx, msg, -1)
    
@bot.command(name="deposit", aliases=["dep"], brief="Deposits money from your cash to your bank")
async def deposit(ctx, usrIn):
    usr = ec.getUser(ctx.author)
    if usrIn == "all": amount = usr.cash
    else:
        try: amount = int(usrIn)
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    usr.deposit(amount)
    await sendEmbed(ctx, f"You deposited ${"{:,}".format(amount)}.", 1)
    
@bot.command(name="withdraw", aliases=["with"], brief="Withdraws money from your bank to your cash")
async def withdraw(ctx, usrIn):
    usr = ec.getUser(ctx.author)
    if usrIn == "all": amount = usr.balance
    else:
        try: amount = int(usrIn)
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    try: usr.withdraw(amount)
    except functions.ErrorToHandle as e: 
        print(f"Error: {e}\nusrIn: {usrIn}\nAmount: {amount}\nBalance: {usr.balance}")
        return await sendEmbed(ctx, f"e", -1)
    await sendEmbed(ctx, f"You withdrew ${"{:,}".format(amount)}.", 1)

@bot.command(name="give", brief="use `.give @<user> <amount>` to give someone else money")
async def give(ctx, giveUser: discord.Member, usrIn):
    usr = ec.getUser(ctx.author)
    if usrIn == "all": amount = usr.cash
    else:
        try: amount = int(usrIn)
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    if amount > usr.cash: return await sendEmbed(ctx, "You cannot give more money than you have! Please withdraw more", -1)
    usr.cash -= amount
    ec.getUser(giveUser).cash += amount
    await sendEmbed(ctx, f"You gave ${"{:,}".format(amount)}. to {giveUser.display_name}", 1)
    
@bot.command(name="leaderboard", aliases=["lb", "baltop", "top", "bt"], brief="Displays the top 10 balances")
async def leaderboard(ctx):
    msg = ""
    place = 1
    for i in ec.leaderboard():
        if place>10: break
        msg+=f"{place}) {i.user.display_name}: {"{:,}".format(i.balance + i.cash)}\n"
        place+=1
    await sendEmbed(ctx, msg)
    
@bot.command(name="blackjack", aliases=["bj"], brief="Allows you to play blackjack")
async def blackjack(ctx, usrIn):
    usr = ec.getUser(ctx.author)
    if usrIn == "all": amount = usr.cash
    else:
        try: amount = int(usrIn)
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    if amount > usr.cash: return await sendEmbed(ctx, "You cannot gamble more money than you have! Please withdraw more", -1)
    data = {
        "usrCards": [random.choice(bjcards), random.choice(bjcards), random.choice(bjcards)],
        "dealerCards": [random.choice(bjcards), random.choice(bjcards), random.choice(bjcards)]
    }
    string, string2 = ""
    for i in data["usrCards"]: string += f"{i} "
    for i in data["dealerCards"]: string2 += f"{i} "
    msg = f"Your Hand: {string}\nDealer Hand: {string2}"
    await sendEmbed(ctx, msg)

@deposit.error
async def deposit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await sendEmbed(ctx, "You need to add an amount!", -1)

@withdraw.error
async def withdraw_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await sendEmbed(ctx, "You need to add an amount!", -1)

@blackjack.error
async def blackjack_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await sendEmbed(ctx, "You need to add an amount!", -1)        

@give.error
async def give_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
        await sendEmbed(ctx, "You need to @ the person you want to give the money to and then add the amount", -1)
# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)