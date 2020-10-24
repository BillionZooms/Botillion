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
        name = await client.fetch_user(mention) #Gets the User from the IDr 
        return name.name
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
    member = await getUserFromMention(name)
    member = ctx.guild.get_member_named(member)
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
    member = await getUserFromMention(name)
    member = ctx.guild.get_member_named(member)
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

@client.command()
async def createroom(ctx, user1 = None, user2 = None, nameoruser3 = None, nameormove = None, move = None):
    user1 = await getUserFromMention(user1)
    user2 = await getUserFromMention(user2)
    user1 = ctx.guild.get_member_named(user1)
    user2 = ctx.guild.get_member_named(user2)
    if user1 == None or user2 == None:
        await ctx.send("You need to enter at least 2 users (maximum 3)")
        return
    categories = ctx.guild.by_category()
    for c in categories:
        for cl in c:
            if cl.id == 756536378363478058:
                category = cl
                break
            else:
                break
    channels = ctx.guild.voice_channels
    if not nameoruser3 == None and nameoruser3.startswith('<@') and nameoruser3.endswith('>'):
        user3 = await getUserFromMention(nameoruser3)
        user3 = ctx.guild.get_member_named(user3)
        if nameormove == None:
            x = 1
            name = 'Private Room #' + str(x)
            for i in channels:
                if name.lower() == i.name.lower():
                    x = x + 1
                    name = 'Private Room #' + str(x)
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                user1: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user2: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user3: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True)
            }
            for l in channels:
                position = l.position + 1
            await ctx.guild.create_voice_channel(name, overwrites=overwrites, position=position, category=category)
        elif nameormove.lower() == 'move':
            x = 1
            name = 'Private Room #' + str(x)
            for i in channels:
                if name.lower() == i.name.lower():
                    x = x + 1
                    name = 'Private Room #' + str(x)
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                user1: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user2: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user3: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True)
            }
            for l in channels:
                position = l.position + 1
            vchannel = await ctx.guild.create_voice_channel(name, overwrites=overwrites, position=position, category=category)
            if ctx.author.guild_permissions.administrator:
                if user1.voice == None or user2.voice == None or user3.voice == None:
                    await ctx.send("All users need to be in voice chat to move.")
                else:
                    await user1.move_to(vchannel)
                    await user2.move_to(vchannel)
                    await user3.move_to(vchannel)
            else:
                ctx.send("Couldn't use the 'move' argument due to lack of permissions.")
        elif not nameormove == None and move.lower() == 'move':
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                user1: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user2: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user3: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True)
            }
            for l in channels:
                position = l.position + 1
            vchannel = await ctx.guild.create_voice_channel(nameormove, overwrites=overwrites, position=position, category=category)
            if ctx.author.guild_permissions.administrator:
                if user1.voice == None or user2.voice == None or user3.voice == None:
                    await ctx.send("All users need to be in voice chat to move.")
                else:
                    await user1.move_to(vchannel)
                    await user2.move_to(vchannel)
                    await user3.move_to(vchannel)
            else:
                ctx.send("Couldn't use the 'move' argument due to lack of permissions.")

        elif not nameormove == None and move.lower() == False:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                user1: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user2: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
                user3: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True)
            }
            for l in channels:
                position = l.position + 1
            vchannel = ctx.guild.create_voice_channel(nameormove, overwrites=overwrites, position=position, category=category)
    elif nameoruser3 == None:
        x = 1
        name = 'Private Room #' + str(x)
        for i in channels:
            if name.lower() == i.name.lower():
                x = x + 1
                name = 'Private Room #' + str(x)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user1: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
            user2: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True)
        }
        for l in channels:
            position = l.position + 1
        await ctx.guild.create_voice_channel(name, overwrites=overwrites, position=position, category=category)
    elif not nameoruser3 == None and nameormove == 'move':
        x = 1
        name = 'Private Room #' + str(x)
        for i in channels:
            if name.lower() == i.name.lower():
                x = x + 1
                name = 'Private Room #' + str(x)
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel = False),
            user1: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True),
            user2: discord.PermissionOverwrite(connect = True, speak = True, view_channel = True)
        }
        for l in channels:
            position = l.position + 1
        vchannel = await ctx.guild.create_voice_channel(nameoruser3, overwrites=overwrites, position=position, category=category)
        if ctx.author.guild_permissions.administrator:
            if user1.voice.channel == None or user2.voice.channel == None:
                await ctx.send("All users need to be in voice chat to move.")
            else:
                await user1.move_to(vchannel)
                await user2.move_to(vchannel)
            
        else:
            ctx.send("Couldn't use the 'move' argument due to lack of permissions.")


client.run('token')