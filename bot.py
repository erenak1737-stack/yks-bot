import discord
from discord.ext import commands, tasks
from datetime import datetime, timezone, timedelta
import feedparser
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
USER_ID = 708319733942059069

TZ_TR = timezone(timedelta(hours=3))

RSS_KAYNAKLAR = [
    ("NTV", "https://www.ntv.com.tr/gundem.rss"),
    ("Hürriyet", "https://www.hurriyet.com.tr/rss/anasayfa"),
    ("Sabah", "https://www.sabah.com.tr/rss/anasayfa.xml"),
    ("Milliyet", "https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml"),
    ("⚽ Hürriyet Spor", "https://www.hurriyet.com.tr/rss/spor"),
    ("🎮 Webtekno", "https://www.webtekno.com/rss.xml"),
]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def haber_al():
    haberler = []
    for kaynak_adi, url in RSS_KAYNAKLAR:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:2]:  # Her kaynaktan 2 haber
                baslik = entry.get("title", "").strip()
                link = entry.get("link", "")
                if baslik:
                    haberler.append((kaynak_adi, baslik, link))
        except Exception:
            continue
    return haberler


def haber_embed():
    simdi = datetime.now(TZ_TR)
    haberler = haber_al()

    embed = discord.Embed(
        title=f"📰 Gündem — {simdi.strftime('%d.%m.%Y')}",
        description="Bugünün öne çıkan haberleri:",
        color=0x2C3E50,
    )

    if not haberler:
        embed.description = "Haberler alınamadı, lütfen daha sonra tekrar dene."
    else:
        for kaynak, baslik, link in haberler:
            embed.add_field(
                name=f"🔹 {kaynak}",
                value=f"[{baslik}]({link})" if link else baslik,
                inline=False,
            )

    embed.set_footer(text=f"⏰ {simdi.strftime('%H:%M')} | Developed by erenzei")
    return embed


@bot.event
async def on_ready():
    print(f"✅ {bot.user.name} olarak giriş yapıldı!")
    gunluk_haber.start()


@tasks.loop(minutes=1)
async def gunluk_haber():
    simdi = datetime.now(TZ_TR)
    if simdi.hour == 10 and simdi.minute == 0:
        kanal = bot.get_channel(CHANNEL_ID)
        if kanal is None:
            print("⚠️ Kanal bulunamadı.")
            return
        await kanal.send(embed=haber_embed())


@gunluk_haber.before_loop
async def baslangic():
    await bot.wait_until_ready()


@bot.command(name="haber")
async def haber_komut(ctx):
    await ctx.send(embed=haber_embed())


bot.run(TOKEN)
