import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix= 'cum.', intents = intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    line = open("responses.txt").read().splitlines()
    if ctx.author.id == 123:
        await ctx.send(f'fuck yourself billion')
    else:
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(line)}')

async def getUserFromMention(mention):
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]
        name = await client.fetch_user(mention)
        name = name.name
        return name
    else:
        return mention

@client.command()
async def blacklist(ctx, *, name):
    guild = ctx.guild
    membername = await getUserFromMention(name)
    member = guild.get_member_named(membername)
    if not member == None:
        bltxt = open("blacklist.txt", "a")
        bltxt.write(f'{name}, ')
        await ctx.send(f'Blacklisted {name} from using commands.')
        bltxt.close()
    else:
        await ctx.send('Member is not in this server.')
    

    
    
    

@client.command()
async def blacklist_list(ctx):
    bltxt = open("blacklist.txt", "r")
    bllist = bltxt.read()
    await ctx.send(f'The blacklisted users are: {bllist}')
    


    
    



client.run('token')