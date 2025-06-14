import discord
from discord.ext import commands
from datetime import datetime
import pytz
import pycountry
import os
from dotenv import load_dotenv
from country_timezones import COUNTRY_TIMEZONES  # 外部ファイルから辞書を読み込む

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} としてログインしました")

@bot.tree.command(name="time", description="国コードから現在時刻を表示します")
async def time(interaction: discord.Interaction, code: str):
    code = code.upper()
    if code in COUNTRY_TIMEZONES:
        country = pycountry.countries.get(alpha_2=code)
        country_name = country.name if country else code
        tz_name = COUNTRY_TIMEZONES[code]
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        await interaction.response.send_message(f"{country_name}（{code}）の現在時刻は：{now}")
    else:
        await interaction.response.send_message("その国コードには対応していません。")

# ボットのトークンを.envから読み込む
load_dotenv()
bot.run(os.environ["DISCORD_BOT_TOKEN"])

