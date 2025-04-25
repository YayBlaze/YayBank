import functions, discord, json

class BankAccount:
    """Bank account class to manage user balance and cash"""
    balance = None
    cash = None
    total = None
    user: discord.Member = None
    cooldowns: {str, int} = {}
    
    def __init__(self, user: discord.Member):
        self.cash = 0
        self.user = user
        self.balance = 0
        
    def toJson(self):
        json = {'cash': self.cash, 'balance': self.balance}
        return json
    
    def loadJson(self, json:dict):
        self.cash = json['cash']
        self.balance = json['balance']
        
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
        # self.accounts = sorted(self.accounts, key=lambda el: (el).cash + el.balance)
        return [item for item in self.accounts.values()]