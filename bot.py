import discord, os, dotenv, time, random
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

async def sendEmbed(ctx, message:str, type:int = 0,):
    if type < 0: color = discord.Color.red()
    elif type > 0: color = discord.Color.green()
    else: color = discord.Color.blurple()
    embed = discord.Embed(color=color)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar)
    embed.description = message
    await ctx.send(embed=embed)
    

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(name="with your money", type=0))
    print(f'{bot.user} is now running')

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')
    
@bot.command(name="balance", aliases=["bal"])
async def balance(ctx):
    usr = ec.getUser(ctx.author)
    msg = f"Cash: ${usr.cash}\nBank: ${usr.balance}\nTotal: ${usr.balance + usr.cash}"
    await sendEmbed(ctx, msg)
    
@bot.command(name="work")
async def work(ctx):
    usr = ec.getUser(ctx.author)
    amount = random.randint(25, 750)
    usr.addMoney(amount)
    msg = functions.getWorkMsg(amount)
    await sendEmbed(ctx, msg, 1)
    
@bot.command(name="deposit", aliases=["dep"])
async def deposit(ctx, usrIn):
    usr = ec.getUser(ctx.author)
    if usrIn == "all": amount = usr.cash
    else:
        try: amount = int(usrIn)
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    usr.deposit(amount)
    await sendEmbed(ctx, f"You deposited ${amount}.", 1)
    
@bot.command(name="withdraw", aliases=["with"])
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
    await sendEmbed(ctx, f"You withdrew ${amount}.", 1)
    
@bot.command(name="leaderboard", aliases=["lb", "baltop", "top", "bt"])
async def leaderboard():
    msg = ""
    for i in ec.leaderboard():
        pass
            

@deposit.error
async def deposit_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await sendEmbed(ctx, "You need to add an amount!", -1)

@withdraw.error
async def withdraw_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await sendEmbed(ctx, "You need to add an amount!", -1)
# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)