import os
import discord
import hmtai
import keep_alive
from waifu import WaifuClient
from discord.ext import commands

intents = discord.Intents.all()
intents.reactions = True

bot = commands.Bot(command_prefix='w!', intents=intents)

@bot.event
async def on_ready():
  print(f'------------------------------')
  print(f'{bot.user.name} Is ONLINE')
  print(f'------------------------------')
  await bot.tree.sync()
  await bot.change_presence(activity=discord.Game(name="With Waifus"))


@bot.tree.command(name = "safewaifu", description = "Fetches A SFW Waifu")
async def sw(interaction, *, message: str = "waifu"):
  categories = [
    "waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug",
    "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile",
    "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill",
    "kick", "happy", "wink", "poke", "dance", "cringe"
  ]
  if message.lower() in categories:
    client = WaifuClient()
    result = client.sfw(category=message)
    await interaction.response.send_message(result)
  else:
    await interaction.response.send_message(
      'Waifu Category Not Found \nPlese Check The Category In `/CategoryWaifu`')


@bot.tree.command(name = "notsafewaifu", description = "Fetches A NSFW Waifu")
async def nw(interaction, *, message: str = "waifu"):
  categories = ["waifu", "neko", "trap", "blowjob"]
  if message.lower() in categories:
    client = WaifuClient()
    result = client.nsfw(category=message)
    await interaction.response.send_message(result)
  else:
    await interaction.response.send_message(
      'Waifu Category Not Found \nPlese Check The Category In `!cwaifu`')


@bot.tree.command(name = "categorywaifu", description = "Fetches The Categories Of Waifu")
async def cw(interaction):
    scategories = [
        " • waifu", "neko",  "bully", "cuddle", "cry", "hug",
        "awoo", "kiss",  "pat", "smug", "bonk", "yeet", "blush", "smile",
        "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill",
        "kick", "happy", "wink", "poke", "dance", "cringe"
    ]

    
    embed = discord.Embed(title="Waifu Emotes", color=0x2f3136)
    
    embed.add_field(name="SWF Waifus", value='\n • '.join(scategories), inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)  

    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name = "dm", description = "DM's You")
async def dm(interaction):
    user = interaction.author
    message = "Hello, Get Started With Naughty Stuffs"
    await user.response.send_message(message)
    await interaction.response.send_message("Message Sent !")

@bot.tree.command(name = "categoryhentai", description = "Fetches The Hentai Categories")
async def ch(interaction):
  hcategories = [' • anal', 'ass','bdsm','cum','classic','creampie','manga','fedom','hentai','incest','masturbation','public','ero','orgy','elves','pantsu','glasses','cuckold','blowjob','boobjob','footjob','handjob','boobs','thigs','pussy','ahegao','uniform','gangbang','gif','nsfwMobileWallpaper','wallpaper']

  embed = discord.Embed(title="Hentai Categories", color=0x2f3136)
  embed.add_field(name=" ", value='\n • '.join(hcategories), inline=True)

  await interaction.response.send_message(embed=embed)

@bot.tree.command(name = "hentai", description = "Fetches A Hentai Image / Gif")
async def h(interaction, *,message: str = "hentai"):
    
    hentai = hmtai.get("hmtai",category=message)
    await interaction.response.send_message(hentai)


@bot.tree.command(name = "nekos", description = "Fetches A Nekos Waifu")
async def n(interaction, *,message: str = "waifu"):
    
    hentai = hmtai.get("nekos",category=message)
    await interaction.response.send_message(hentai)



keep_alive.keep_alive()

token = os.environ['TOKEN']
bot.run(token)
