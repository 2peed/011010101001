import json
import nextcord
import os

class Settings:
    def __init__(self):
        
        with open(os.path.join(os.path.dirname(__file__), "settings.json")) as f:
            sett = json.load(f)

        # TOKEN artık .env dosyasından alınacak
        self.token = os.getenv("TOKEN")

        self.svrid = sett["server-id"]
        self.catid = sett["category-id"]
        self.vcid = sett["vc-id"]
        self.color = int(sett["embed-color"], 16)
        self.prefix = sett["prefix"]
        self.state = nextcord.Game(name="Speed Cookin'up Art?")
