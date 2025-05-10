import random, json

class ErrorToHandle(Exception):
    """Exception raised for custom error in the application."""
    message = "generic error message"

    def __init__(self, message):
        self.message = message
        super().__init__(message)

    def __str__(self):
        return f"{self.message}"

def getWorkMsg(amount):
    with open("work_msgs.json") as f:
        templates = json.load(f)
    template = random.choice(templates)
    return template.replace(":coin: {amount}", f":coin: {amount}")

def getCrimeWin(amount):
    with open("crime_win.json") as f:
        templates = json.load(f)
    template = random.choice(templates)
    return template.replace(":coin: {amount}", f":coin: {amount}")

def getCrimeLose(amount):
    with open("crime_fail.json") as f:
        templates = json.load(f)
    template = random.choice(templates)
    return template.replace(":coin: {amount}", f":coin: {amount}")

cardList = ["<:as:1365940170066628649>", "<:2s:1365939494523506829>", "<:3s:1365939572214730832>", "<:4s:1365939637683486750>", "<:5s:1365939698719264778>", "<:6s:1365939766519926884>", "<:7s:1365939847209947156>", "<:8s:1365939925450621028>", "<:9s:1365940002177159249>", "<:10s:1365940085102608384>", "<:js:1365940382310993923>", "<:qs:1365940560111603712>", "<:ks:1365940474925285426>", "<:ah:1365940142686077010>", "<:2h:1365939480095100930>", "<:3h:1365939557446582313>", "<:4h:1365939616074563654>", "<:5h:1365939683095216239>", "<:6h:1365939743522689084>", "<:7h:1365939827500912700>", "<:8h:1365939908560294080>", "<:9h:1365939983562838087>", "<:10h:1365940055432233071>", "<:jh:1365940342284877834>", "<:qh:1365940542671814746>", "<:kh:1365940448279138344>", "<:ac:1365940107911368764>", "<:2c:1365939446268166185>", "<:3c:1365939525523734558>", "<:4c:1365939585502285884>", "<:5c:1365939652174807090>", "<:6c:1365939713000738917>", "<:7c:1365939789567758386>", "<:8c:1365939864238952461>", "<:9c:1365939946032201790>", "<:10c:1365940020288032868>", "<:jc:1365940292091641887>", "<:qc:1365940499235606599>", "<:kc:1365940405832519761>", "<:ad:1365940126399598652>", "<:2d:1365939465859760189>", "<:3d:1365939542678306826>", "<:4d:1365939601935437855>", "<:5d:1365939665236004896>", "<:6d:1365939727047458847>", "<:7d:1365939807167189003>", "<:8d:1365939884707151962>", "<:9d:1365939964583346216>", "<:10d:1365940037727944767>", "<:jd:1365940315407650897>", "<:qd:1365940522375450624>", "<:kd:1365940428293148773>"]
rouletteOptions = ["red", "black", "even", "odd", "1-18", "19-36"]