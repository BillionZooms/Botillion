from discord.ext import commands

async def getUserFromMention(bot, mention):
    if mention.startswith('<@') and mention.endswith('>'):
        mention = mention[2:-1]
        if mention.startswith('!'):
            mention = mention[1:]
        name = await bot.fetch_user(mention)
        return name.name
    else:
        return mention

async def checkUserinList(listx, userid):
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

def countTrueMembers(guild):
    count = 0
    for i in guild.members:
        if not i.bot:
            count += 1
    return count

def countBots(guild):
    count = 0
    for i in guild.members:
        if i.bot:
            count += 1
    return count