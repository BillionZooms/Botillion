import discord
import asyncio
from discord.ext import commands
import random
import json

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix= '.', intents = intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await client.change_presence()

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

def tempchannelAdd(userid, channelid):
    with open('tempchannel.json', 'r') as f:
        try:
            d = json.load(f)
            if userid in d['Owners'].keys():
                l = d['Owners'].get(userid)
                l.append(channelid)
                d['Owners'][userid] = l
            else:
                di = {
                    userid : idlist[channelid]
                }
                d['Owners'].update(di)
        except:
            idlist = []
            idlist.append(channelid)
            d = {
                'Owners' : {
                    userid : idlist
                }
            }
        f.close()
    with open('tempchannel.json', 'w') as f:
        json.dump(d, f, indent=2)
        f.close()
        

@client.command()
async def croom(ctx, user1, user2, *args):
    categories = ctx.guild.by_category()
    user1, user2 = await getUserFromMention(user1), await getUserFromMention(user2)
    user1, user2 = ctx.guild.get_member_named(user1), ctx.guild.get_member_named(user2)
    name = None
    for c in categories:
        for cl in c:
            if cl.id == 756536378363478058:
                category = cl
                break
            else:
                break
    channels = ctx.guild.voice_channels
    move = False
    userlist = [user1, user2]
    if user1 == None or user2 == None:
        await ctx.send("Please give at least 2 users to create a room.")
        return
    for i in range(0,len(args)):
        puser = await getUserFromMention(args[i])
        user = ctx.guild.get_member_named(puser)
        if user != None:
            userlist += [user]
        elif args[i].lower() == 'move':
            move = True
            break
        else:
            name = args[i]
    if move == True:
        permissions = {}
        permissions[ctx.guild.default_role] = discord.PermissionOverwrite(view_channel = False)
        if name == None:
            x = 1
            name = 'Private Room #' + str(x)
            for i in channels:
                if name.lower() == i.name.lower():
                    x = x + 1
                    name = 'Private Room #' + str(x)
        for user in userlist:
            permissions[user] = discord.PermissionOverwrite(view_channel = True)
        for l in channels:
            position = l.position + 1
        vchannel = await ctx.guild.create_voice_channel(name, overwrites=permissions, position=position, category=category)
        for role in ctx.author.roles:
            if role.id == 770364408848842853:
                rperm = True
                break
            else:
                rperm = False
        if rperm == True:
            for user in userlist:
                if user.voice == None:
                    await ctx.send(f"Couldnt move : {user.mention} they are not in a voice channel.")
                else:
                    await user.move_to(vchannel)
        else:
            await ctx.send("Couldn't use the 'move' argument due to lack of role.")
    else:
        permissions = {}
        permissions[ctx.guild.default_role] = discord.PermissionOverwrite(view_channel = False)
        if name == None:
            x = 1
            name = 'Private Room #' + str(x)
            for i in channels:
                if name.lower() == i.name.lower():
                    x = x + 1
                    name = 'Private Room #' + str(x)
        for user in userlist:
            permissions[user] = discord.PermissionOverwrite(view_channel = True)
        for l in channels:
            position = l.position + 1
        vchannel = await ctx.guild.create_voice_channel(name, overwrites=permissions, position=position, category=category)
        tempchannelAdd(str(ctx.author.id), vchannel.id)

@client.command(aliases=['croom.clear', 'clear room', 'room clear', 'clear', 'clear_croom', 'clear.croom'])
async def croom_clear(ctx):
    user = str(ctx.author.id)
    with open('tempchannel.json', 'r') as f:
        d = json.load(f)
        if user in d['Owners'].keys():
            while len(d['Owners'][user]) != 0:
                for channels in d['Owners'][user]:
                    for i in ctx.guild.voice_channels:
                        if i.id == channels:
                            listid = d['Owners'][user]
                            await i.delete()
                            listid.remove(channels)
                            d['Owners'][user] = listid
        else:
            await ctx.send("You haven't created a room yet! Use `.croom user1 user2` to create a room.")
            return
        del d['Owners'][user]
        f.close()

    with open('tempchannel.json', 'w') as f:
        json.dump(d, f)
        f.close()
        
client.run('token')