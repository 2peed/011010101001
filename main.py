import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from settings import *
from room import *
import datetime
import asyncio
import os
import threading
from flask import Flask

# =====================
# UPTIME WEB SERVER
# =====================
app = Flask(__name__)

@app.route("/")
def home():
    return "", 200

def run_web():
    port = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

threading.Thread(target=run_web).start()

# =====================
# DISCORD BOT
# =====================
settings = Settings()
roomlist = []
bruteforce = []

client = commands.Bot(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print("Bot online")
    await client.change_presence(activity=settings.state)
    while True:
        bruteforce.clear()
        await asyncio.sleep(60)

@client.slash_command(guild_ids=[settings.svrid], description="Bot gecikmesini öğrenin.")
async def ping(inter: Interaction):
    embed = nextcord.Embed(
        title="Pong!",
        description=f"Gecikme süresi: {str(client.latency)[0:4]}",
        color=settings.color
    )
    await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızı adlandırın.", name="adlandır")
async def rename(inter: Interaction, ad: str):
    for room in roomlist:
        if room.owner == inter.user.id:
            await room.obj.edit(name=ad)
            embed = nextcord.Embed(title="Başarılı!", description="Odan başarıyla adlandırıldı.", color=settings.color)
            return await inter.response.send_message(embed=embed)

    embed = nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color)
    await inter.response.send_message(embed=embed)

# --- DİĞER TÜM KOMUTLARIN ---
# (HİÇ DOKUNULMADI, AYNEN SENİN ATTIĞIN GİBİ)

@client.event
async def on_voice_state_update(member, before, after):
    try:
        if after.channel.id == settings.vcid:
            channel = await member.guild.create_voice_channel(
                str(member.display_name),
                category=nextcord.utils.get(member.guild.categories, id=settings.catid),
                user_limit=1
            )
            roomlist.append(Room(channel.id, member.id, channel))
            await member.move_to(channel)
            embed = nextcord.Embed(
                title="Hoşgeldin!",
                description="Özel sohbet odan hazır!",
                color=settings.color
            )
            await member.send(embed=embed)
    except:
        pass

    try:
        for room in roomlist:
            if room.id == before.channel.id and room.count() == 0:
                await room.delete()
                roomlist.remove(room)
    except:
        pass

    try:
        if after.channel:
            for room in roomlist:
                if after.channel.id == room.id:
                    if room.mode == 1 and member.id in room.blacklist:
                        await member.move_to(None)
                    elif room.mode == 0 and member.id not in room.whitelist:
                        await member.move_to(None)
    except Exception as e:
        print(e)

# =====================
# TOKEN (.env / Render ENV)
# =====================
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
