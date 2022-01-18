# bot.py
import os
import re
import json
import discord
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.environ['DISCORD_TOKEN']

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))

bot = commands.Bot(command_prefix="?")
@bot.command(name="shodan")
async def some_crazy_function_name(ctx, args):
  if is_valid_ip(args):
    shodan_result = requests.get("https://internetdb.shodan.io/" + args)
    shodan_json = json.loads(shodan_result.content)

    if("detail" in shodan_json and shodan_json["detail"] == "No information available"):
      await ctx.channel.send("Error: No information availible for this IP address.")
    else:
      DESCRIPTION="Shodan InternetDB Results For " + args
      embed=discord.Embed(title=DESCRIPTION, color=0xdf0000)
      embed.add_field(name="Hostnames", value=shodan_json["hostnames"], inline=False)
      embed.add_field(name="Open Ports", value=shodan_json["ports"], inline=False)
      embed.add_field(name="Tags", value=shodan_json["tags"], inline=False)
      embed.add_field(name="CPEs", value=shodan_json["cpes"], inline=False)
      embed.add_field(name="Vulns", value=shodan_json["vulns"], inline=False)
      await ctx.send(embed=embed)
  else:
    await ctx.channel.send("Error: Invalid IP Address.")

bot.run(TOKEN)
