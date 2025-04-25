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