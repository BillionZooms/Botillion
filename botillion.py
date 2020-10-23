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
    if mention.startswith('<@') and mention.endswith('>'):  #If its a mention, removes the <@ and >
        mention = mention[2:-1]
        if mention.startswith('!'): #Removes an '!' if its at the start of the ID.
            mention = mention[1:]
        name = await client.fetch_user(mention) #Gets the User from the ID
        name = name.name    #Get the name of the User 
        return name
    else:
        return mention

async def checkUserinList(listx, userid):           #Returns True if the userid is found in the given file.
    b = False
    readfile = open(listx, "r")
    read = readfile.readline()
    while read:
        newnumber = ""
        for i in read:
            if i != ' ':
                newnumber = newnumber + i
            else:
                break
        if newnumber == userid:
            b = True
            break
        else:
            b = False
            read = readfile.readline()
    return b

@client.command()
async def blacklist(ctx, *, name):          #blacklist || Blacklists a user and saves the ID to blacklist.txt. Admin only.
    guild = ctx.guild
    membername = await getUserFromMention(name)
    member = guild.get_member_named(membername)
    if ctx.author.guild_permissions.administrator:
        if member == None:
            await ctx.send('Member is not in this server.')
        alreadyBl = await checkUserinList("blacklist.txt", str(member.id))
        if alreadyBl == True:
            await ctx.send("User is already blacklisted.")
        else:
            if not member == None:
                bltxt = open("blacklist.txt", "a")
                bltxt.write(f'{member.id} {member.name}#{member.discriminator}\n')
                await ctx.send(f'Blacklisted {member.mention} from using commands.')
                bltxt.close()    
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
    
client.run('')