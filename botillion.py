import discord
import asyncio
from discord.ext import commands
import random
import json
import logging

logg = logging.getLogger(__name__)
logg.setLevel('DEBUG')

streamhandler = logging.StreamHandler()
formatt = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
streamhandler.setFormatter(formatt)

logg.addHandler(streamhandler)


intents = discord.Intents.all()
client = commands.Bot(command_prefix= '.', intents = intents)
extensions = ['cogs.misc', 'cogs.admin', 'cogs.org', 'cogs.corp']

@client.event
async def on_ready():
    logg.info('We have logged in as {0.user}'.format(client))
        
if __name__ == '__main__':
    for extension in extensions:
        try:
            client.load_extension(extension)
        except:
            logg.exception("Couldn't load %s", extension)
    with open('token.txt', 'r') as f:
        token = f.read()
        client.run(token)
