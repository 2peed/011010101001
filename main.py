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
# UPTIME WEB SERVER (Flask)
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
# INTENTS
# =====================
intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

# =====================
# DISCORD BOT
# =====================
settings = Settings()
roomlist = []
bruteforce = []

client = commands.Bot(command_prefix=settings.prefix, intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} online!")
    await client.change_presence(activity=settings.state)
    while True:
        bruteforce.clear()
        await asyncio.sleep(60)

# =====================
# SLASH COMMANDS
# =====================

# Ping
@client.slash_command(guild_ids=[settings.svrid], description="Bot gecikmesini öğrenin.")
async def ping(inter: Interaction):
    embed = nextcord.Embed(title="Pong!", description=f"Gecikme: {str(client.latency)[:4]}", color=settings.color)
    await inter.response.send_message(embed=embed)

# Adlandır
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızı adlandırın.", name="adlandır")
async def rename(inter: Interaction, ad: str):
    for room in roomlist:
        if room.owner == inter.user.id:
            await room.obj.edit(name=ad)
            return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Odan başarıyla adlandırıldı.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Beyaz Liste
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanıza girebilecek kişileri belirleyin.", name="beyaz-liste")
async def whitelist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.addwhitelist(kullanıcı.id)
            return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Kullanıcı başarı ile beyaz listeye eklendi.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Beyaz Liste Kaldır
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızın beyaz listesinden bir kullanıcıyı kaldırın.", name="beyaz-liste-kaldır")
async def unwhitelist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            try:
                room.whitelist.remove(kullanıcı.id)
                return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Kullanıcı başarı ile beyaz listeden kaldırıldı.", color=settings.color))
            except:
                return await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Kullanıcı beyaz listede bulunamadı.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Kara Liste
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanıza giremeyecek kişileri belirleyin.", name="kara-liste")
async def blacklist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.addblacklist(kullanıcı.id)
            return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Kullanıcı başarı ile kara listeye eklendi.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Kara Liste Kaldır
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızın kara listesinden bir kullanıcıyı kaldırın.", name="kara-liste-kaldır")
async def unblacklist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            try:
                room.blacklist.remove(kullanıcı.id)
                return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Kullanıcı başarı ile kara listeden kaldırıldı.", color=settings.color))
            except:
                return await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Kullanıcı kara listede bulunamadı.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Liste Modu
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızda kara liste mi (1) yoksa beyaz liste mi (0) kullanılacağını belirtin.", name="mod-belirle")
async def setmode(inter: Interaction, liste_numarası: int):
    for room in roomlist:
        if room.owner == inter.user.id:
            if liste_numarası in [0,1]:
                room.mode = liste_numarası
                return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Liste modu değiştirildi.", color=settings.color))
            else:
                return await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Geçersiz liste numarası.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Limit Belirle
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanıza kullanıcı limiti belirleyin", name="limit-belirle")
async def setlimit(inter: Interaction, limit: int):
    for room in roomlist:
        if room.owner == inter.user.id:
            if limit > 99:
                return await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Discord'un maksimum kullanıcı limiti 99.", color=settings.color))
            await room.obj.edit(user_limit=limit)
            return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Kullanıcı limiti başarıyla ayarlandı.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# At
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızı bir kullanıcıyı atın", name="at")
async def kick(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            if kullanıcı in room.obj.members:
                await kullanıcı.move_to(None)
                return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Kullanıcı atıldı.", color=settings.color))
            return await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Kullanıcı odanda değil.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Sil
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızı silin.", name="sil")
async def delete(inter: Interaction):
    for room in roomlist:
        if room.owner == inter.user.id:
            await room.delete()
            roomlist.remove(room)
            return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Sohbet odan silindi.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# Devret
@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızı başka birine devredin", name="devret")
async def setowner(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.owner = kullanıcı.id
            return await inter.response.send_message(embed=nextcord.Embed(title="Başarılı!", description="Sohbet odası devredildi.", color=settings.color))
    await inter.response.send_message(embed=nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color))

# =====================
# VOICE STATE UPDATE & BRUTEFORCE
# =====================
@client.event
async def on_voice_state_update(member, before, after):
    try:
        if after.channel and after.channel.id == settings.vcid:
            channel = await member.guild.create_voice_channel(
                str(member.display_name),
                category=nextcord.utils.get(member.guild.categories, id=settings.catid),
                user_limit=1
            )
            roomlist.append(Room(channel.id, member.id, channel))
            await member.move_to(channel)
            await member.send(embed=nextcord.Embed(title="Hoşgeldin!", description="Özel sohbet odan hazır!", color=settings.color))
    except:
        pass

    try:
        for room in roomlist:
            if before.channel and room.id == before.channel.id and room.count() == 0:
                await room.delete()
                roomlist.remove(room)
    except:
        pass

    try:
        if after.channel:
            for room in roomlist:
                if after.channel.id == room.id:
                    # Kara liste / beyaz liste & brute-force
                    if room.mode == 1 and member.id in room.blacklist:
                        await member.move_to(None)
                        await handle_bruteforce(member)
                    elif room.mode == 0 and member.id not in room.whitelist:
                        await member.move_to(None)
                        await handle_bruteforce(member)
    except Exception as e:
        print(e)

async def handle_bruteforce(member):
    for mem in bruteforce:
        if mem[0] == member.id:
            mem[1] += 1
            if mem[1] >= 4:
                await member.edit(timeout=nextcord.utils.utcnow() + datetime.timedelta(seconds=200))
                bruteforce.remove(mem)
                await member.send(embed=nextcord.Embed(title="Tamam yeter!", description="Odaya sürekli girmeye çalıştığın için cezalandırıldın!", color=settings.color))
            return
    bruteforce.append([member.id, 1])
    await member.send(embed=nextcord.Embed(title="Hey hey!", description="Bu odaya giremezsin!", color=settings.color))

# =====================
# RUN
# =====================
TOKEN = os.getenv("TOKEN")
client.run(TOKEN)
