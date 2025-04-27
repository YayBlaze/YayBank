import functions, discord, time

class BankAccount:
    """Bank account class to manage user balance and cash"""
    balance = None
    cash = None
    total = None
    user: discord.Member = None
    cooldowns: {str, int} = {"work": 0, "crime": 0, "bj": 0}
    
    def __init__(self, user: discord.Member):
        self.cash = 0
        self.user = user
        self.balance = 0
        
    def toJson(self):
        json = {'cash': self.cash, 'balance': self.balance, 'cool': self.cooldowns}
        return json
    
    def loadJson(self, json:dict):
        self.cash = json['cash']
        self.balance = json['balance']
        self.cooldowns = json['cool']
        
    def addMoney(self, amount):
        self.cash += amount
    
    def deposit(self, amount):
        if amount > 0:
            if amount > self.cash:
                raise functions.ErrorToHandle("Not enough cash to deposit")
            self.cash -= amount
            self.balance += amount
    
    def withdraw(self, amount):
        if 0 < amount:
            if amount > self.balance:
                raise functions.ErrorToHandle("Not enough balance to withdraw")
            self.balance -= amount
            self.cash += amount
            
    def setCoolDown(self, type, s):
        self.cooldowns[type] = round(time.time()+s)
    def isCool(self, type):
        return self.cooldowns[type] <= time.time()

class Economy:
    """Economy class to manage user accounts and transactions"""
    
    accounts: {discord.Member, BankAccount} = {}
    
    
    def __init__(self):
        pass
    
    def getUser(self, user: discord.Member) -> BankAccount:
        """Get the user from the database"""
        if user in self.accounts: return self.accounts[user]
        else:
            self.accounts[user] = BankAccount(user)
            return self.accounts[user]
        
    def leaderboard(self) -> dict[str, BankAccount]:
        return sorted(self.accounts.values(), key=lambda el: (el.cash + el.balance), reverse=True)
        # def sort(account: BankAccount) -> int:
        #     return  account.cash+account.balance
        # return sorted(self.accounts.values(), key=sort)