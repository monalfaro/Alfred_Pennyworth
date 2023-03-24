import os
import requests
import discord
import asyncio
import random
from requests_html import HTMLSession
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = commands.Bot(intents=discord.Intents().all(), command_prefix="Alfred, ")

@bot.event
async def on_ready():
    print(f'{bot.user} is connected to the following guilds:\n')
    for guild in bot.guilds:
        print(f'- {guild} (ID: {guild.id})\n')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(f'I encountered an error. Don\'t worry, Master {ctx.author.id}. Things always get worse before they get better."')

@bot.command(name="set_timer", help='Sets a timer for the specified number of minutes')
async def set_timer(ctx, minutes: int):
    seconds = minutes * 60
    message = await ctx.send(f'Timer: {seconds//60} minutes left')
    while seconds>0:
        seconds -= 1
        if seconds%60 == 0:
            minutes = seconds // 60
            if minutes>1:
                await message.edit(content=f'Timer: {seconds//60} minutes left')
            else: 
                await message.edit(content=f'Timer: {seconds//60} minute left')
        await asyncio.sleep(1)
    await message.edit(content=f'Timer: 0 minutes left')
    await ctx.send(content=f'The timer {ctx.author.name} set for {minutes} minutes has ended.')

@bot.command(name='magic_8_ball', help='Simulates a Magic 8 Ball')
async def magic_eight_ball(ctx):
    magic_eight_ball_answers = [
        'It is certain.',
        'Don\'t count on it.',
        'As I see it, yes.',
        'You can rely on it.',
        'Ask again later',
        'My sources say no.',
        'The outlook is not so good.',
        'Very doubtful...',
        'Concentrate and ask again.',
        'The signs point to yes.',
        'It is likely.',
    ]
    response = random.choice(magic_eight_ball_answers)
    await ctx.send(response)
       
@bot.command(name="google", help='Returns 1 search result from Google')
async def google(ctx, *args):
    google_url = 'https://google.com/search?q='
    for arg in args:
        google_url+=f"+{arg}"
    try:
        session = HTMLSession()
        response = session.get(google_url)
        links = list(response.html.absolute_links)
        results = []
        for link in links:
            if 'google' not in link:
                results.append(link)
        if len(results)>0:
            await ctx.send(results[0])
        else:
            await ctx.send(f'Apologies, Master {ctx.author.id}, I could not find anything on Google.')
    except requests.exceptions.RequestException as exception:
        print(exception)

bot.run(TOKEN)