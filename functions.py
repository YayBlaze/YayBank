import random, json

class ErrorToHandle(Exception):
    """Exception raised for custom error in the application."""

    def __init__(self, message):
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"

def getWorkMsg(amount):
    with open("work_msgs.json") as f:
        templates = json.load(f)
    template = random.choice(templates)
    return template.replace("${amount}", f"${amount}")

def getCrimeWin(amount):
    with open("crime_win.json") as f:
        templates = json.load(f)
    template = random.choice(templates)
    return template.replace("${amount}", f"${amount}")

def getCrimeLose(amount):
    with open("crime_fail.json") as f:
        templates = json.load(f)
    template = random.choice(templates)
    return template.replace("${amount}", f"${amount}")

cardList = ["SA", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10", "SJ", "SQ", "SK", "HA", "H2", "H3", "H4", "H5", "H6", "H7", "H8", "H9", "H10", "HJ", "HQ", "HK", "CA", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10", "CJ", "CQ", "CK", "DA", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10", "DJ", "DQ", "DK"] #still need to put emoji names in bruh. if you do this, make sure to keep the order. suit order doesnt matter (OCD or smth idk), but card value does.