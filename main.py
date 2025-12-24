import os
from dotenv import load_dotenv

load_dotenv()

import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions, CheckFailure, check, MissingPermissions
from nextcord import Interaction
from settings import *
from room import *
import datetime
import asyncio

client = nextcord.Client()

settings = Settings()
roomlist = []
bruteforce = []

client = commands.Bot(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print("Bot online")
    await client.change_presence(activity=settings.state)
    while True:
        bruteforce = []
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
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanıza girebilecek kişileri belirleyin.", name="beyaz-liste")
async def whitelist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.addwhitelist(kullanıcı.id)
            embed = nextcord.Embed(title="Başarılı!", description="Kullanıcı beyaz listeye eklendi.", color=settings.color)
            return await inter.response.send_message(embed=embed)

    embed = nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanızın beyaz listesinden bir kullanıcıyı kaldırın.", name="beyaz-liste-kaldır")
async def unwhitelist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            try:
                room.whitelist.remove(kullanıcı.id)
                embed = nextcord.Embed(title="Başarılı!", description="Kullanıcı beyaz listeden kaldırıldı.", color=settings.color)
                return await inter.response.send_message(embed=embed)
            except:
                break

    embed = nextcord.Embed(title="Hata!", description="Kullanıcı bulunamadı.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid], description="Sohbet odanıza giremeyecek kişileri belirleyin.", name="kara-liste")
async def blacklist(inter: Interaction, kullanıcı: nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.addblacklist(kullanıcı.id)
            embed = nextcord.Embed(title="Başarılı!", description="Kullanıcı kara listeye eklendi.", color=settings.color)
            return await inter.response.send_message(embed=embed)

    embed = nextcord.Embed(title="Hata!", description="Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

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
            if before.channel and room.id == before.channel.id and room.count() == 0:
                await room.delete()
                roomlist.remove(room)
    except:
        pass

client.run(os.getenv("TOKEN"))
