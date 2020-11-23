import discord
from discord.ext import commands

from cogs.utilsb import users

class Corporation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def nigga(self, ctx):
        if ctx.invoked_subcommand == None:
            achi = ctx.guild.get_member(707654465116831856)
            embed1 = discord.Embed(title = 'Nigga Corp™', description = "'Making the world a better place. One nigga at a time. ;)' - achi", color = 1914860)
            embed1.set_thumbnail(url = str(achi.avatar_url))
            for i in ctx.command.commands:
                embed1.add_field(name = i.name, value = i.description, inline = False)
            await ctx.send(embed = embed1)
    
    @commands.has_role(756946902661988362)
    @nigga.command(description = 'Add the N word role to a given user.')
    async def add(self, ctx, member: discord.Member):
        nrole = ctx.guild.get_role(779413421753368607)
        if not nrole in member.roles:
            await member.add_roles(nrole, reason = 'Given the N word pass by achi.')
            embed1 = discord.Embed(title = 'Success!', description = f"Given {member.mention} the '{nrole.name}' role", color = 1914860)
            await ctx.send(embed = embed1)
        else:
            await ctx.send("User already has the role.")
    
    @commands.has_role(756946902661988362)
    @nigga.command(description = 'Remove the N word role from a given user.')
    async def remove(self, ctx, member: discord.Member):
        nrole = ctx.guild.get_role(779413421753368607)
        if not nrole in member.roles:
            await ctx.send("User doesn't have the role.")
        else:
            await member.remove_roles(nrole)
            embed1 = discord.Embed(title = 'Success!', description = f"Removed the '{nrole.name}' role from '{member.mention}'", color = 1914860)
            await ctx.send(embed = embed1)
            

def setup(bot):
    bot.add_cog(Corporation(bot))