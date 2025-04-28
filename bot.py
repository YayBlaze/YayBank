import discord, os, dotenv, time, random, json, copy
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
    file = open("save.json", "w", encoding="utf-8")
    saveJson = {}
    for i in ec.accounts:
        saveJson[i.id] = ec.accounts[i].toJson()
    # print(saveJson)
    json.dump(saveJson, file)
    file.close()

def load():
    file = open("save.json", "r", encoding="utf-8")
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

@bot.command(brief="Returns your card if the bot is online")
async def magic(ctx):
    await ctx.send('Was THIS <:3c:1365939525523734558> your card?')
    
@bot.command(name="balance", aliases=["bal"], brief="Displays your balance. Use `.balance @<username>` to see the balance of someone else")
async def balance(ctx, target:discord.Member = None):
    if target == None: target = ctx.author
    usr = ec.getUser(target)
    msg = f"Cash: :coin: {"{:,}".format(usr.cash)}\nBank: :coin: {"{:,}".format(usr.balance)}\nTotal: :coin: {"{:,}".format(usr.balance + usr.cash)}"
    await sendEmbed(ctx, msg, usr=target)
    
@bot.command(name="work", brief="Gives you a small amount of money. Has cooldown")
async def work(ctx):
    usr = ec.getUser(ctx.author)
    if usr.isCool("work"):
        amount = random.randint(25, 750)
        usr.addMoney(amount)
        msg = functions.getWorkMsg(amount)
        usr.setCoolDown("work", 30)
        await sendEmbed(ctx, msg, 1)
    else: await sendEmbed(ctx, f"You can you this command again <t:{usr.cooldowns["work"]}:R>", -1)
    
@bot.command(name="crime", brief="Gives you a large amount of money but there is a chance you lose money. Has cooldown")
async def crime(ctx):
    usr = ec.getUser(ctx.author)
    if usr.isCool("crime"):
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
        usr.setCoolDown("crime", 3600)
    else: await sendEmbed(ctx, f"You can you this command again <t:{usr.cooldowns["crime"]}:R>", -1)
        
    
@bot.command(name="deposit", aliases=["dep"], brief="Deposits money from your cash to your bank")
async def deposit(ctx, usrIn):
    usr = ec.getUser(ctx.author)
    if usrIn == "all": amount = usr.cash
    else:
        try: amount = int(usrIn)
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    usr.deposit(amount)
    await sendEmbed(ctx, f"You deposited :coin: {"{:,}".format(amount)}.", 1)
    
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
    await sendEmbed(ctx, f"You withdrew :coin: {"{:,}".format(amount)}.", 1)

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
    await sendEmbed(ctx, f"You gave :coin: {"{:,}".format(amount)}. to {giveUser.display_name}", 1)

@bot.command(name="rob", brief="use .rob <user> to steal money from them")
async def rob(ctx, stealUser: discord.Member):
    target = ec.getUser(stealUser)
    usr = ec.getUser(ctx.author)
    if not usr.isCool('rob'): return await sendEmbed(ctx, f"You can use this command again in <t:{usr.cooldowns["rob"]}:R>", -1)
    if target.cash <=0:
        usr.setCoolDown("rob", 600)
        return await sendEmbed(ctx, "That user doesn't have any cash!", -1)
    else:
        amount = round((target.cash) * random.uniform(0.25, 0.7))
        if bool(random.getrandbits(1)):
            target.cash -= amount
            usr.cash += amount
            await sendEmbed(ctx, f"You stole :coin: {amount} from {stealUser.display_name}", 1)
        else:
            usr.cash -= amount
            await sendEmbed(ctx, f"You got caught trying to steal from {stealUser.display_name} and was fined :coin: {amount}", -1)

    
@bot.command(name="leaderboard", aliases=["lb", "baltop", "top", "bt"], brief="Displays the top 10 balances")
async def leaderboard(ctx):
    msg = ""
    place = 1
    for i in ec.leaderboard():
        if place>10: break
        msg+=f"{place}) {i.user.display_name}: {"{:,}".format(i.balance + i.cash)}\n"
        place+=1
    await sendEmbed(ctx, msg)

@bot.command(name="taxes", aliases=["tax"], brief="Command you use to pay taxes")
async def taxes(ctx):
    usr = ec.getUser(ctx.author)
    place = 1
    for i in ec.leaderboard():
        if place > 3: return await sendEmbed(ctx, "You don't owe any taxes!", 1)
        if i.user == ctx.author: 
            amount = round((usr.balance+usr.cash) * 0.025)
            usr.cash -= amount
            ec.socialSecurity += amount
            return await sendEmbed(ctx, f"You have paid :coin: {amount} in taxes.", -1)
        place+=1
    
    
@bot.command(name="blackjack", aliases=["bj"], brief="Allows you to play blackjack")
async def blackjack(ctx, usrIn):
    usr = ec.getUser(ctx.author)
    if not usr.isCool("bj"): #checks if the cooldown has worn off
        await sendEmbed(ctx, f"You can play blackjack again in <t:{usr.cooldowns["bj"]}:R>", -1) #if it hasnt, deny the user to gamble
    if usrIn == "all": amount = usr.cash #set gamble amount to all cash if "all"
    else:
        try: amount = int(usrIn) #otherwise try to make it a number
        except ValueError: return await sendEmbed(ctx, "Please enter a number or all", -1)
    if amount < 200: return await sendEmbed(ctx, "You must place at least :coin: 200 for your bet", -1)
    if amount > usr.cash: return await sendEmbed(ctx, "You cannot gamble more money than you have! Please withdraw more", -1)
    availableCards = copy.deepcopy(cardList) #have a local copy of the card list
    aces = [] #list of ace emojis (not filled out)
    tensCards = [] #list of cards with a value over 9 (not filled out)
    dealerCards = [] #new list for the dealer's cards
    playerCards = [] #new list for the player's cards
    dealerTempValue = 0 #temp 'working' value for dealer's cards
    dealerValue = 0 #final value for dealer's cards (the one displayed to user)
    playerTempValue = 0 #same for player
    playerValue = 0 #same for player
    for i in range(2): #draw the first two cards
        dealerCards.append(random.choice(availableCards)) #add a random card
        availableCards.pop(cardList.index(dealerCards[i])) #remove the card from the local list of cards
        playerCards.append(availableCards[12]) #repeat add - rigged at the moment
        availableCards.pop(cardList.index(playerCards[i])) #repeat remove
    Result = await sendEmbed(ctx, f"Hit: Draw another card \n Stand: keep your cards \n Dealer: {cardList.index(dealerCards[0])} \n {dealerCards[0]} :blue_square: \n Player: bruh i dont wanna do that math rn \n {playerCards[0]} {playerCards[1]}")
    if set(playerCards).intersection(aces) and set(playerCards).intersection(tensCards): #if the player has a blackjack (having an ace and a card greater than 9)
        if set(dealerCards).intersection(aces) and set(dealerCards).intersection(tensCards): #if the dealer also has a blackjack
            await Result.edit(ctx, f"Result: Push money back \n Dealer: Blackjack \n {dealerCards[0]} {dealerCards[1]} \n Player: Blackjack \n {playerCards[0]} {playerCards[1]}") #womp womp money back, should in theory edit the og message
        else: #otherwise only player has blackjack, and therefore wins
            Spoils = usrIn * 1.5 #calculate the spoils, multiplied by 1.5 because blackjack
            if set(dealerCards).intersection(aces): #determine dealer value (soft number, ie ace=11)
                if dealerCards[0] in aces: #which one is which #1
                    dealerValue = cardList.index(dealerCards[1]) #get the card index value from the OG card list
                    while dealerValue > 12: #get the value between 0 and 12
                        dealerValue -= 13
                    dealerValue += 1 #add one, accounting for index, and you get the value of the card
                else: #hm must be the other one then
                    dealerValue = cardList.index(dealerCards[0])
                    while dealerValue > 12:
                        dealerValue -= 13
                    dealerValue += 1
            else: #neither of the dealer's cards are aces
                for i in range(2): #repeat through both cards
                    dealerTempValue = cardList.index(dealerCards[i]) #add the value to the temp list to manipulate it
                    while dealerTempValue > 12: #make it between 0 and 12
                        dealerTempValue -= 13
                    dealerTempValue += 1 #add 1, now you have the card's value
                    dealerValue += dealerTempValue #add the temp value to the final value, and repeat for the second card
            await Result.edit(ctx, f"Result: Dealer busts :coin: {Spoils} \n Dealer: Soft {dealerValue} \n {dealerCards[0]} {dealerCards[1]} \n Player: Blackjack \n {playerCards[0]} {playerCards[1]}", 1) #Player W, should edit the message
    #else: #lmao you didn't immediately get a blackjack? (currently commented so it doesn't throw an error)
        #player hit or stand, buttons and editing messages should be interesting :)
        await sendEmbed(ctx, "You didn't get a blackjack! You lose ig because i haven't coded this part yet", -1)
        


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