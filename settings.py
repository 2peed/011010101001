import json
import nextcord

class Settings:
    def __init__(self):
        
        with open("settings.json") as f:
            sett = json.loads(f.read())
            f.close()

        
        self.svrid = sett["server-id"]
        self.catid = sett["category-id"]
        self.vcid = sett["vc-id"]
        self.color = int(sett["embed-color"], 16)
        self.prefix = sett["prefix"]
        self.state = nextcord.Game(name="Speed on fire boy?")
