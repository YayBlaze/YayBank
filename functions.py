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

bjcards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]