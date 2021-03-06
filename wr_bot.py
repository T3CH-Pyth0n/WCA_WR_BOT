import discord
from bs4 import BeautifulSoup as bs
from discord.ext import commands
from urllib import request, error
import json
from config import *
client = commands.Bot(command_prefix=prefix)

event_dict = {'333': '3x3',
              '444': '4x4',
              '555': '5x5',
              '666': '6x6',
              '777': '7x7',
              '222': '2x2',
              'skewb': 'skewb',
              'sq1': 'squan',
              '333bf': '3BLD',
              '444bf': '4BLD',
              '555bf': '5BLD',
              '333mbf': 'MBLD',
              '333oh': 'OH',
              'minx': 'Megaminx',
              'pyram': 'pyraminx',
              'clock': 'clock',
              '333fm': 'fmc'}

event_dic2 = {'3x3': '333',
              '4x4': '444',
              '5x5': '555',
              '6x6': '666',
              '7x7': '777',
              '2x2': '222',
              'skewb': 'skewb',
              'squan': 'sq1',
              '3BLD': '333bf',
              '4BLD': '444bf',
              '5BLD': '555bf',
              'MBLD': '333mbf',
              'OH': '333oh',
              'Megaminx': 'minx',
              'pyraminx': 'pyram',
              'clock': 'clock',
              'fmc': '333fm'}


def data_ext(event):
    cube_page = request.urlopen(f'https://www.worldcubeassociation.org/results/rankings/{event}/single')
    soup = bs(cube_page, 'html.parser')
    rank_table = soup.find('tbody')
    ranks = rank_table.find_all("tr")[0:]
    positions = []
    names = []
    results = []
    for rank in ranks:
        positions.append(rank.find('td', class_="pos").text)
        names.append(rank.find('td', class_="name").a.text)
        results.append(rank.find('td', class_="result").text)
    return f"{names[0]}: {results[0]}"


@client.event
async def on_ready():
    print("bot is ready")


@client.command(name="WR!")
async def world_record(ctx, event_name):
    if event_name in event_dict.values():
        data = data_ext(event_dic2[event_name])

        await ctx.send(data)
    else:
        await ctx.send("Enter proper event name.")


@client.command(name='comp_no?')
async def comp_no(ctx, wca_id):

        data = request.urlopen(f"https://www.worldcubeassociation.org/api/v0/persons/{wca_id}")
        data = json.load(data)
        await ctx.send(f"no. of comps: {data['competition_count']}")


@client.command(name='events')
async def events(ctx, wca_id):
    try:
        data = json.load(request.urlopen(f"https://www.worldcubeassociation.org/api/v0/persons/{wca_id}"))
        new = data['personal_records'].keys()
        event123 = ''
        for i in new:
            event123 += event_dict[i] + "\n"
        await ctx.send(event123)

    except error.HTTPError:
        pass


@client.command(name='PR_AVG!')
async def pr_avg(ctx, wca_id, ev):
    data = json.load(request.urlopen(f"https://www.worldcubeassociation.org/api/v0/persons/{wca_id}"))
    if ev in event_dic2.keys():
        if event_dic2[ev] in data['personal_records'].keys():
            raw_pr = int(data['personal_records'][event_dic2[ev]]['average']['best'])
            decimal = raw_pr % 100
            int_ = int(raw_pr/100)
            if int_ > 60:
                await ctx.send(f"{int(int_/60)}:{int_ % 60}.{decimal}")
            else:
                await ctx.send(f"{int_}.{decimal}")


@client.command(name='PR_SINGLE!')
async def pr_single(ctx, wca_id, ev):
    data = json.load(request.urlopen(f"https://www.worldcubeassociation.org/api/v0/persons/{wca_id}"))
    if ev in event_dic2.keys():
        if event_dic2[ev] in data['personal_records'].keys():
            raw_pr = int(data['personal_records'][event_dic2[ev]]['single']['best'])
            decimal = raw_pr % 100
            int_ = int(raw_pr/100)
            if int_ > 60:
                await ctx.send(f"{int(int_/60)}:{int_ % 60}.{decimal}")
            else:
                await ctx.send(f"{int_}.{decimal}")



print(json.load(request.urlopen(f"https://www.worldcubeassociation.org/api/v0/persons/2018PATE06")))

client.run(token)