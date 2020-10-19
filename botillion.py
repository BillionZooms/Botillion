import discord
from discord.ext import commands
import random

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix= 'cum.', intents = intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(aliases=['8ball'])          #8BALL || Takes question and in return sends and answer randomly pulled from responses.txt with random.choice
async def _8ball(ctx, *, question):
    line = open("responses.txt").read().splitlines()
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(line)}')

async def getUserFromMention(mention):          #Transforms a mention into a username. Example : <@147840568897044480> to billion
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]
        name = await client.fetch_user(mention)
        name = name.name
        return name
    else:
        return mention

async def checkUserinList(listx, userid):           #Returns True if the userid is found in the given file.
    b = False
    try: 
        readfile = open(listx, "r")
        read = readfile.readline()
        while read:
            if read.endswith('\n'):
                read = read[:-1]
                if read == userid:
                    b = True
                    break
                else:
                    b = False
                    read = readfile.readline()
            else:
                print('idk')
    except:
        print("Error checkUserinList")
    return b

@client.command()
async def blacklist(ctx, *, name):          #blacklist || Blacklists a user and saves the ID to blacklist.txt. Admin only.
    guild = ctx.guild
    membername = await getUserFromMention(name)
    member = guild.get_member_named(membername)
    if ctx.author.guild_permissions.administrator:
        alreadyBl = await checkUserinList("blacklist.txt", str(member.id))
        if alreadyBl == True:
            await ctx.send("User is already blacklisted.")
        else:
            if not member == None:
                bltxt = open("blacklist.txt", "a")
                bltxt.write(f'{member.id}\n')
                await ctx.send(f'Blacklisted {member.mention} from using commands.')
                bltxt.close()
            else:
                await ctx.send('Member is not in this server.')
    else:
        await ctx.send("Only people with Administrator privileges are allowed to use this command!")

@client.command()
async def unblacklist(ctx, *, name):            #unblacklist || Unblacklists a user and removes their name from blacklist.txt
    guild = ctx.guild
    membername = await getUserFromMention(name)
    member = guild.get_member_named(membername)
    if ctx.author.guild_permissions.administrator:
        isBl = await checkUserinList("blacklist.txt", str(member.id))
        if isBl == True:
            with open("blacklist.txt", "r+") as f:
                d = f.readlines()
                f.seek(0)
                for i in d:
                    if i.endswith('\n'):
                        i = i[:-1]
                        if i != str(member.id):
                            f.write(f'{i}\n')
                        else:
                            await ctx.send("User is now un-blacklisted.")
                f.truncate()
        else:
            await ctx.send("User is not blacklisted or doesn't exist.")
    else:
        await ctx.send("Only people with Administrator privileges are allowed to use this command!")


@client.command()
async def blacklist_list(ctx):
    bltxt = open("blacklist.txt", "r")
    bllist = bltxt.read()
    await ctx.send(f'The blacklisted users are: {bllist}')
    
client.run('token')