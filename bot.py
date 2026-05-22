import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
USER_ID = 708319733942059069

# TYT: 20 Haziran 2026 - 10:15 (Türkiye saati UTC+3)
TZ_TR = timezone(timedelta(hours=3))
YKS_DATETIME = datetime(2026, 6, 20, 10, 15, 0, tzinfo=TZ_TR)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def sure_hesapla():
    simdi = datetime.now(TZ_TR)
    fark = YKS_DATETIME - simdi
    toplam_saniye = int(fark.total_seconds())

    if toplam_saniye <= 0:
        return None  # Sınav geçti

    gun = fark.days
    kalan_saniye = toplam_saniye - (gun * 86400)
    saat = kalan_saniye // 3600
    dakika = (kalan_saniye % 3600) // 60

    return gun, saat, dakika


def yks_embed():
    simdi = datetime.now(TZ_TR)
    sure = sure_hesapla()

    if sure is None:
        embed = discord.Embed(
            title="✅ YKS Tamamlandı",
            description="YKS sınavı geçti. Başarılar dileriz!",
            color=0xE74C3C,
        )
        embed.set_footer(text="Developed by erenzei")
        return embed

    gun, saat, dakika = sure

    if gun == 0 and saat == 0 and dakika == 0:
        embed = discord.Embed(
            title="🎉 Bugün YKS Günü!",
            description="Tüm adaylara bol şans! 🍀",
            color=0x2ECC71,
        )
        embed.set_footer(text="Developed by erenzei")
        return embed

    embed = discord.Embed(
        title="📚 YKS TYT Geri Sayım",
        description=f"**{gun} gün {saat} saat {dakika} dakika kaldı!**",
        color=0x3498DB,
    )
    embed.add_field(name="🗓️ Sınav Tarihi", value="20 Haziran 2026 - Cumartesi", inline=True)
    embed.add_field(name="⏰ Sınav Saati", value="10:15", inline=True)
    embed.add_field(name="📆 Şu An", value=simdi.strftime("%d.%m.%Y %H:%M"), inline=True)
    embed.set_footer(text="Çalış, başarı gelecek! 💪 | Developed by erenzei")
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
