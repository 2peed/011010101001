import json
import nextcord
import os  # bunu ekledik, token için

class Settings:
    def __init__(self):
        
        with open("settings.json") as f:
            sett = json.loads(f.read())
            f.close()

        # TOKEN artık burada yok, .env dosyasından alınacak
        self.token = os.getenv("TOKEN")  # Token artık burada da okunabilir, opsiyonel

        self.svrid = sett["server-id"]
        self.catid = sett["category-id"]
        self.vcid = sett["vc-id"]
        self.color = int(sett["embed-color"], 16)
        self.prefix = sett["prefix"]
        self.state = nextcord.Game(name="Speed Cookin'up Art?")
