import discord
from discord.ext import commands, tasks
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
USER_ID = 708319733942059069

# YKS TYT tarihi — gerekirse değiştir
YKS_DATE = date(2026, 6, 14)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def gun_hesapla():
    bugun = date.today()
    return (YKS_DATE - bugun).days


def yks_embed():
    kalan = gun_hesapla()
    bugun_str = date.today().strftime("%d.%m.%Y")
    yks_str = YKS_DATE.strftime("%d.%m.%Y")

    if kalan > 0:
        embed = discord.Embed(
            title="📚 YKS Geri Sayım",
            description=f"**YKS'ye {kalan} gün kaldı!**",
            color=0x3498DB,
        )
        embed.add_field(name="🗓️ Sınav Tarihi", value=yks_str, inline=True)
        embed.add_field(name="📆 Bugün", value=bugun_str, inline=True)
        embed.set_footer(text="Çalış, başarı gelecek! 💪 | Developed by erenzei")
    elif kalan == 0:
        embed = discord.Embed(
            title="🎉 Bugün YKS Günü!",
            description="Tüm adaylara bol şans! 🍀",
            color=0x2ECC71,
        )
    else:
        embed = discord.Embed(
            title="✅ YKS Tamamlandı",
            description=f"YKS sınavı **{abs(kalan)} gün önce** gerçekleşti.",
            color=0xE74C3C,
        )
    return embed


@bot.event
async def on_ready():
    print(f"✅ {bot.user.name} olarak giriş yapıldı!")
    saatlik_bildirim.start()


@tasks.loop(hours=1)
async def saatlik_bildirim():
    kanal = bot.get_channel(CHANNEL_ID)
    if kanal is None:
        print("⚠️  Kanal bulunamadı — CHANNEL_ID'yi kontrol et.")
        return
    await kanal.send(content=f"<@{USER_ID}>", embed=yks_embed())


@saatlik_bildirim.before_loop
async def bildirim_baslangic():
    await bot.wait_until_ready()


@bot.command(name="yks")
async def yks_komut(ctx):
    await ctx.send(content=f"<@{USER_ID}>", embed=yks_embed())

@bot.command(name="komut")
async def komut(ctx):
    await ctx.send(content=f"<@{USER_ID}>", embed=yks_embed())


bot.run(TOKEN)
