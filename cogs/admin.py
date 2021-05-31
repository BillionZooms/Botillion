import discord
from discord.ext import commands

from cogs.utilsb import users


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden = True)
    async def blacklist(self, ctx, *, name):
        member = await users.getUserFromMention(self.bot, name)
        member = ctx.guild.get_member_named(member)
        if ctx.author.guild_permissions.administrator:
            if member == None:
                await ctx.send('Member is not in this server.')
                return
            alreadyBl = await users.checkUserinList("blacklist.txt", str(member.id))
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
    
    @commands.command(hidden = True)
    async def unblacklist(self, ctx, *, name = None):
        if name == None:
            return await ctx.send("Please mention the user you want unblacklisted")
        member = await users.getUserFromMention(self.bot, name)
        member = ctx.guild.get_member_named(member)
        if member == None:
            await ctx.send("Couldn't find user named {0}".format(name))
            return
        if ctx.author.guild_permissions.administrator:
            isBl = await users.checkUserinList("blacklist.txt", str(member.id))
            if isBl == True:
                with open("blacklist.txt", "r+") as f:
                    d = f.readlines()
                    f.seek(0)
                    for i in d:
                        tempid = ''
                        for x in i:
                            if not x == ' ':
                                tempid += str(x)
                            else:
                                break
                        if tempid != str(member.id):
                            f.write(f'{i}\n')
                    await ctx.send("User is now un-blacklisted.")
                    f.truncate()
                    f.close()
            else:
                await ctx.send("User is not blacklisted or doesn't exist.")
        else:
            await ctx.send("Only people with Administrator privileges are allowed to use this command!")

    @commands.command(hidden = True)
    async def blacklist_list(self, ctx):
        bltxt = open("blacklist.txt", "r")
        bllist = bltxt.read()
        await ctx.send(f'The blacklisted users are:\n`{bllist}`')

    @commands.command(hidden = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):
        await member.kick(reason = reason)
        embed = discord.Embed(title = 'Success!', description = f'Sucessfully kicked {member.mention}')
        await ctx.send(embed = embed)
        


def setup(bot):
    bot.add_cog(Admin(bot))