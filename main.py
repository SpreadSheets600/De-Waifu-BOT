import os
import hmtai
import discord
import datetime
import requests
import keep_alive
from ping3 import ping
from waifu import WaifuClient
from discord.ext import commands
from AnilistPython import Anilist

intents = discord.Intents.all()
intents.reactions = True

bot = commands.Bot(command_prefix='w!', intents=intents)

API_ENDPOINT = 'https://api-aniwatch.onrender.com/anime/home'
SCHEDULE_API_ENDPOINT = 'https://api-aniwatch.onrender.com/anime/schedule'

@bot.event
async def on_ready():
  print(f'------------------------------')
  print(f'{bot.user.name} Is ONLINE')
  print(f'------------------------------')
  await bot.tree.sync()
  await bot.change_presence(activity=discord.Game(name="With Waifus"))

@bot.tree.command(name='animetoday', description='Fetches Today\'s Anime Schedule')
async def animetoday(interaction):
    try:
        today_date = datetime.now().strftime('%Y-%m-%d')

        request_url = f"{SCHEDULE_API_ENDPOINT}?date={today_date}"

        response = requests.get(request_url)
        data = response.json()

        embed = discord.Embed(title=f"Today's Scheduled Anime - {today_date}", color=discord.Color.blue())

        for anime in data['scheduledAnimes']:
            embed.add_field(
                name=f"{anime['time']} - {anime['name']}",
                value=f"Japanese Name : {anime['jname']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f'Error Fetching Today\'s Anime Schedule : {e}')
        await interaction.response.send_message('Error Fetching Today\'s Anime Schedule. Please Try Again Later.')

@bot.tree.command(name='trending', description='Fetches Trending Animes')
async def trending(interaction):
    try:
        response = requests.get(API_ENDPOINT)
        data = response.json()

        embed = discord.Embed(title='Trending Anime', color=discord.Color.blue())

        for anime in data['trendingAnimes']:
            embed.add_field(
                name=f"{anime['rank']}. {anime['name']}",
                value=f"Episode : {anime['episodes']['sub']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f'Error Fetching Anime: {e}')
        await interaction.response.send_message('Error Fetching Anime. Please Try Again Later.')

@bot.tree.command(name='spotlight', description='Fetches Spotlight Animes')
async def spotilight(interaction):
    try:
        response = requests.get(API_ENDPOINT)
        data = response.json()

        embed = discord.Embed(title='Spotlight Animes', color=discord.Color.blue())

        for anime in data['spotlightAnimes']:
            embed.add_field(
                name=f"{anime['rank']}. {anime['name']}",
                value=f"Episode: {anime['episodes']['sub']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f'Error Fetching Anime: {e}')
        await interaction.response.send_message('Error Fetching Anime. Please Try Again Later.')

@bot.tree.command(name='latest', description='Fetches Latest Episodes')
async def latest(interaction):
    try:
        response = requests.get(API_ENDPOINT)
        data = response.json()

        embed = discord.Embed(title='Latest Episodes', color=discord.Color.blue())

        for anime in data['latestEpisodeAnimes']:
            embed.add_field(
                name=f"{anime['name']}",
                value=f"Episode: {anime['episodes']['sub']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    except Exception as e:
        print(f'Error Fetching Anime: {e}')
        await interaction.response.send_message('Error Fetching Latest Episode. Please Try Again Later.')

@bot.tree.command(name="anisearch", description="search for anime")
async def anisearch(interaction, *, anime_name: str):
  try:
    anime_dict = anilist.get_anime(anime_name=anime_name)

    anime_id = anilist.get_anime_id(anime_name)
    anime_desc = anime_dict['desc']
    anime_title = anime_dict["name_english"]
    starting_time = anime_dict["starting_time"]
    ending_time = anime_dict["ending_time"]
    next_airing_ep = anime_dict["next_airing_ep"]
    airing_format = anime_dict["airing_format"]
    airing_status = anime_dict["airing_status"]
    airing_ep = anime_dict["airing_episodes"]
    season = anime_dict["season"]
    genres = anime_dict["genres"]
    anime_url = f'https://anilist.co/anime/{anime_id}/'
    cover_image = anime_dict["banner_image"]

    next_ep_string = ''
    try:
      initial_time = next_airing_ep['timeUntilAiring']
      mins, secs = divmod(initial_time, 60)
      hours, mins = divmod(mins, 60)
      days, hours = divmod(hours, 24)
      timer = f'{days} days {hours} hours {mins} mins {secs} secs'
      next_ep_num = next_airing_ep['episode']
      next_ep_string = f'Episode {next_ep_num} is releasing in {timer}!\
                            \n\n[{anime_title} AniList Page]({anime_url}))'

    except:
      next_ep_string = f"This Anime's Release Date Has Not Been Confirmed Yet.\
                            \n\n[{anime_title} AniList Page]({anime_url}))"

    if anime_desc != None and len(anime_desc) != 0:
      anime_desc = anime_desc.split("<br>")

    anime_embed = discord.Embed(title=anime_title, color=0xA0DB8E)
    anime_embed.set_image(url=cover_image)
    anime_embed.add_field(name="Synopsis", value=anime_desc[0], inline=False)
    anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
    anime_embed.add_field(name="Anime ID", value=anime_id, inline=True)
    anime_embed.add_field(name="Airing Date", value=starting_time, inline=True)
    anime_embed.add_field(name="Ending Date", value=ending_time, inline=True)
    anime_embed.add_field(name="Season", value=season, inline=True)

    try:
      episodes = int(airing_ep)

      if episodes > 1:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({airing_ep} Episodes)",
                              inline=True)
      else:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({airing_ep} Episode)",
                              inline=True)

    except:
      anime_embed.add_field(name="Airing Format",
                            value=airing_format,
                            inline=True)

    if airing_status.upper() == 'FINISHED':
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
      anime_embed.add_field(name="Genres",
                            value=", ".join(genres),
                            inline=False)
      anime_embed.add_field(
          name="Next Episode ~",
          value=
          f"The Anime Has Finished Airing !\n\n[{anime_title} AniList Page]({anime_url})\n",
          inline=False)

    else:
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="Genres", value=genres, inline=True)
      anime_embed.add_field(name="Next Episode ~",
                            value=next_airing_ep,
                            inline=False)

    await interaction.response.send_message(embed=anime_embed)

  except Exception as e:
    print(e)
    await interaction.response.send_message(f'An Error Occured Searching For Anime \n```Error :  {e}```'
                   )


@bot.tree.command(name="mangasearch", description="search for manga")
async def mangasearch(interaction, *, anime_name):
  try:
    manga_dict = anilist.get_manga(anime_name)

    manga_id = anilist.get_manga_id(anime_name)
    manga_desc = manga_dict['desc']
    manga_title = manga_dict["name_english"]
    starting_time = manga_dict["starting_time"]
    ending_time = manga_dict["ending_time"]
    airing_format = manga_dict["release_format"]
    chapters = manga_dict["chapters"]
    airing_status = manga_dict["release_status"]
    season = manga_dict["volumes"]
    genres = manga_dict["genres"]
    anime_url = f'https://anilist.co/manga/{manga_id}/'
    cover_image = manga_dict["banner_image"]

    if manga_desc != None and len(manga_desc) != 0:
      manga_desc = manga_desc.split("<br>")

    anime_embed = discord.Embed(title=manga_title, color=0xA0DB8E)
    anime_embed.set_image(url=cover_image)
    anime_embed.add_field(name="Synopsis", value=manga_desc[0], inline=False)
    anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
    anime_embed.add_field(name="Manga ID", value=manga_id, inline=True)
    anime_embed.add_field(name="Release Date",
                          value=starting_time,
                          inline=True)
    anime_embed.add_field(name="Ending Date", value=ending_time, inline=True)
    anime_embed.add_field(name="Volume", value=season, inline=True)

    try:
      episodes = int(chapters)

      if episodes > 1:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({chapters} Chapters)",
                              inline=True)
      else:
        anime_embed.add_field(name="Airing Format",
                              value=f"{airing_format} ({chapters} Chapter)",
                              inline=True)

    except:
      anime_embed.add_field(name="Airing Format",
                            value=airing_format,
                            inline=True)

    if airing_status.upper() == 'FINISHED':
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="\u200b", value="\u200b", inline=False)
      anime_embed.add_field(name="Genres",
                            value=", ".join(genres),
                            inline=False)
      anime_embed.add_field(
          name="Next Episode ~",
          value=
          f"The Manga Has Finished It's Release !\n\n[{manga_title} AniList Page]({anime_url})\n",
          inline=False)

    else:
      anime_embed.add_field(name="Airing Status",
                            value=airing_status,
                            inline=True)
      anime_embed.add_field(name="Genres", value=genres, inline=True)

    await interaction.response.send_message(embed=anime_embed)

  except Exception as e:
    print(e)
    await interaction.response.send_message(f'An Error Occured Searching For Anime \n```Error :  {e}```'
                   )


@bot.tree.command(name="charactersearch", description="search for character")
async def charactersearch(interaction, *, character_name):

  character_dict = anilist.get_character(character_name)
  character_id = anilist.get_character_id(character_name)

  character_desc = character_dict['desc']
  first_name = character_dict["first_name"]
  last_name = character_dict["last_name"]
  image = character_dict["image"]

  if last_name != None:
    character_name = str(first_name) + str(last_name)
  else:
    character_name = str(first_name)

  if character_desc and len(character_desc) > 1024:
    character_desc = character_desc[:970] + f"[ ... Read More. ](https://anilist.co/character/{character_id})"

  try:
    character_embed = discord.Embed(title=character_name, color=0xA0DB8E)
    character_embed.set_image(url=image)
    character_embed.add_field(name="Description",
                              value=character_desc,
                              inline=False)
    character_embed.add_field(name="\u200b", value="\u200b", inline=False)
    character_embed.add_field(name="Character Name",
                              value=character_name,
                              inline=True)
    character_embed.add_field(name="Character ID",
                              value=character_id,
                              inline=True)

    await interaction.response.send_message(embed=character_embed)

  except Exception as e:
    print(e)
    await interaction.response.send_message(
        f'An Error Occured Searching For Character \n```{e}```')


@bot.tree.command(name="help", description="Displays Help Message")
async def help(interaction):
  help_embed = None
  help_embed = discord.Embed(title="Help",
                             description="List Of Available Commands",
                             color=0xA0DB8E)

  help_embed.set_image(url="https://shorturl.at/bju12")
  help_embed.add_field(name="`>help`",
                       value="Display This Help Message",
                       inline=False)
  help_embed.add_field(name="`>anisearch`",
                       value="Search For An Anime",
                       inline=False)
  help_embed.add_field(name="`>mangasearch`",
                       value="Search For A Manga",
                       inline=False)
  help_embed.add_field(name="`>characterseach`",
                       value="Search For A Character",
                       inline=False)
  await interaction.response.send_message(embed=help_embed)


@bot.tree.command(name="ping", description="Displays Bot's Ping")
async def ping(interaction):

  latency = bot.latency * 1000
  server_name = interaction.guild.name if interaction.guild else "Direct Message"
  uptime = datetime.datetime.now() - bot.start_time
  uptime_seconds = uptime.total_seconds()
  uptime_str = str(datetime.timedelta(seconds=uptime_seconds)).split(".")[0]
  num_servers = len(bot.guilds)

  embed = discord.Embed(title="_*Pong !*_", color=0xA0DB8E)
  embed.add_field(name="---------------------", value="     ", inline=False)
  embed.add_field(name="Servers", value=num_servers, inline=False)
  embed.add_field(name="Latency", value=f"{latency:.2f}ms", inline=False)
  embed.add_field(name="Server Name", value=server_name, inline=False)
  embed.add_field(name="Uptime", value=uptime_str, inline=False)

  await interaction.response.send_message(embed=embed)

@bot.tree.command(name = "safewaifu", description = "Fetches A SFW Waifu")
async def sw(interaction, *, message: str = "waifu"):
  categories = [
    "waifu", "neko", "shinobu", "megumin", "bully", "cuddle", "cry", "hug",
    "awoo", "kiss", "lick", "pat", "smug", "bonk", "yeet", "blush", "smile",
    "wave", "highfive", "handhold", "nom", "bite", "glomp", "slap", "kill",
    "kick", "happy", "wink", "poke", "dance", "cringe"
  ]
  if message.lower() in categories:
    bot = Waifubot()
    result = bot.sfw(category=message)
    await interaction.response.send_message(result)
  else:
    await interaction.response.send_message(
      'Waifu Category Not Found \nPlese Check The Category In `/CategoryWaifu`')


@bot.tree.command(name = "notsafewaifu", description = "Fetches A NSFW Waifu")
async def nw(interaction, *, message: str = "waifu"):
  categories = ["waifu", "neko", "trap", "blowjob"]
  if message.lower() in categories:
    bot = Waifubot()
    result = bot.nsfw(category=message)
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
