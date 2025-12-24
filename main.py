import nextcord
from nextcord.ext import commands, tasks
from nextcord.ext.commands import has_permissions,  CheckFailure, check, MissingPermissions
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

@client.slash_command(guild_ids=[settings.svrid],description="Bot gecikmesini öğrenin.")
async def ping(inter : Interaction):
    #embedVar = discord.Embed(title="Title", description="Desc", color=0x00ff00)
    #embedVar.add_field(name="Field1", value="hi", inline=False)
    #embedVar.add_field(name="Field2", value="hi2", inline=False)
    embed = nextcord.Embed(title="Pong!", description=f"Gecikme süresi: {str(client.latency)[0:4]}", color=settings.color)
    await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızı adlandırın.",name="adlandır")
async def rename(inter : Interaction, ad : str):
    for room in roomlist:
        if room.owner == inter.user.id:
            await room.obj.edit(name=ad)
            embed = nextcord.Embed(title="Başarılı!", description=f"Odan başarıyla adlandırıldı.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanıza girebilecek kişileri belirleyin.",name="beyaz-liste")
async def whitelist(inter : Interaction, kullanıcı : nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.addwhitelist(kullanıcı.id)
            embed = nextcord.Embed(title="Başarılı!", description=f"Kullanıcı başarı ile beyaz listeye eklendi.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızın beyaz listesinden bir kullanıcıyı kaldırın.",name="beyaz-liste-kaldır")
async def unwhitelist(inter : Interaction, kullanıcı : nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            try:
                idx = room.whitelist.index(kullanıcı.id)
                room.whitelist.pop(idx)
                embed = nextcord.Embed(title="Başarılı!", description=f"Kullanıcı başarı ile beyaz listeden kaldırıldı.", color=settings.color)
                return await inter.response.send_message(embed=embed)
            except:
                embed = nextcord.Embed(title="Hata!", description=f"Kullanıcı beyaz listede bulunamadı.", color=settings.color)
                return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanıza giremeyecek kişileri belirleyin.",name="kara-liste")
async def blacklist(inter : Interaction, kullanıcı : nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.addblacklist(kullanıcı.id)
            embed = nextcord.Embed(title="Başarılı!", description=f"Kullanıcı başarı ile kara listeye eklendi.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızın kara listesinden bir kullanıcıyı kaldırın.",name="kara-liste-kaldır")
async def unblacklist(inter : Interaction, kullanıcı : nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            try:
                idx = room.blacklist.index(kullanıcı.id)
                room.blacklist.pop(idx)
                embed = nextcord.Embed(title="Başarılı!", description=f"Kullanıcı başarı ile kara listeden kaldırıldı.", color=settings.color)
                return await inter.response.send_message(embed=embed)
            except:
                embed = nextcord.Embed(title="Hata!", description=f"Kullanıcı kara listede bulunamadı.", color=settings.color)
                return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızda kara liste mi (1) yoksa beyaz liste mi (0) kullanılacağını belirtin.",name="mod-belirle")
async def setmode(inter : Interaction, liste_numarası : int):
    for room in roomlist:
        if room.owner == inter.user.id:
            if liste_numarası == 1 or liste_numarası == 0:
                room.mode = liste_numarası
            else:
                embed = nextcord.Embed(title="Hata!", description=f"Geçersiz liste numarası. Lütfen belirtilen numaraları kullanın:\n`Kara liste: 1`\n`Beyaz liste: 0`", color=settings.color)
                return await inter.response.send_message(embed=embed)

            embed = nextcord.Embed(title="Başarılı!", description=f"Liste modu değiştirildi.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanıza kullanıcı limiti belirleyin",name="limit-belirle")
async def setlimit(inter : Interaction, limit : int):
    for room in roomlist:
        if room.owner == inter.user.id:
            if limit > 99:
                embed = nextcord.Embed(title="Hata!", description=f"Discord'un maksimum kullanıcı limiti 99.", color=settings.color)
                return await inter.response.send_message(embed=embed)

            await room.obj.edit(user_limit=limit)

            embed = nextcord.Embed(title="Başarılı!", description=f"Kullanıcı limiti başarıyla ayarlandı.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızdan bir kullanıcıyı atın",name="at")
async def kick(inter : Interaction, kullanıcı:nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            if kullanıcı in room.obj.members:
                await kullanıcı.move_to(None)
                embed = nextcord.Embed(title="Başarılı!", description=f"Kullanıcı sohbet odandan atıldı", color=settings.color)
                return await inter.response.send_message(embed=embed)

            embed = nextcord.Embed(title="Hata!", description=f"Kullanıcı sohbet odanda değil.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızı silin.",name="sil")
async def delete(inter : Interaction):
    for room in roomlist:
        if room.owner == inter.user.id:
            await room.delete()

            embed = nextcord.Embed(title="Başarılı!", description=f"Sohbet odan silindi.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.slash_command(guild_ids=[settings.svrid],description="Sohbet odanızı başka birine devredin",name="devret")
async def setowner(inter : Interaction, kullanıcı:nextcord.Member):
    for room in roomlist:
        if room.owner == inter.user.id:
            room.owner = kullanıcı.id

            embed = nextcord.Embed(title="Başarılı!", description=f"Sohbet odası kullanıcıya devredildi.", color=settings.color)
            return await inter.response.send_message(embed=embed)
    
    embed = nextcord.Embed(title="Hata!", description=f"Şuanda özel bir sohbet odan yok.", color=settings.color)
    return await inter.response.send_message(embed=embed)

@client.event
async def on_voice_state_update(member, before, after):
    try:
        if after.channel.id == settings.vcid:
            channel = await member.guild.create_voice_channel(str(member.display_name), category=nextcord.utils.get(member.guild.categories, id=settings.catid), user_limit=1)
            roomlist.append(Room(channel.id, member.id, channel))
            await member.move_to(channel)
            embed = nextcord.Embed(title="Hoşgeldin!", description=f"Özel sohbet odan hazır, komutları kullanarak özelleştirebilirsin!", color=settings.color)
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
        if after.channel != None:
            for room in roomlist:
                if after.channel.id == room.id:
                    if room.mode == 1:
                        if member.id in room.blacklist:
                            await member.move_to(None)
                            for mem in bruteforce:
                                if mem[0] == member.id:
                                    if mem[1] >= 4:
                                        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=200))
                                        bruteforce.remove(mem)
                                        embed = nextcord.Embed(title="Tamam yeter!", description=f"Anlaşılan odaya devamlı olarak girmeye çalışarak kullanıcıları rahatsız ediyorsun ve beni meşgul ediyorsun?\nCezanı alacaksın o zaman!", color=settings.color)
                                        return await member.send(embed=embed)
                            embed = nextcord.Embed(title="Hey hey!", description=f"Kara listede olduğun için bu odaya giremezsin.", color=settings.color)
                            await member.send(embed=embed)
                            for mem in bruteforce:
                                if mem[0] == member.id:
                                    mem[1] += 1
                                    return
                            bruteforce.append([member.id, 1])
                            
                    elif room.mode == 0:
                        if member.id not in room.whitelist:
                            await member.move_to(None)
                            for mem in bruteforce:
                                if mem[0] == member.id:
                                    if mem[1] >= 4:
                                        await member.edit(timeout=nextcord.utils.utcnow()+datetime.timedelta(seconds=200))
                                        bruteforce.remove(mem)
                                        embed = nextcord.Embed(title="Tamam yeter!", description=f"Anlaşılan odaya devamlı olarak girmeye çalışarak kullanıcıları rahatsız ediyorsun ve beni meşgul ediyorsun?\nCezanı alacaksın o zaman!", color=settings.color)
                                        return await member.send(embed=embed)
                            embed = nextcord.Embed(title="Hey hey!", description=f"Beyaz listede olmadığın için bu odaya giremezsin.", color=settings.color)
                            await member.send(embed=embed)
                            for mem in bruteforce:
                                if mem[0] == member.id:
                                    mem[1] += 1
                                    return
                            bruteforce.append([member.id, 1])
    except Exception as e:
        print(e)

client.run(process.env.token)