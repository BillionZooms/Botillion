import discord
from discord.ext import commands

import json
import logging
import os
import random

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = '8ball')
    async def _8ball(self, ctx, *, question):
        line = open('responses.txt', 'r').read().splitlines()
        img = ctx.author.avatar_url
        embcolor = discord.Colour(294120)
        embed = discord.Embed(colour=embcolor)
        embed.set_thumbnail(url=img)
        embed.add_field(name='Question', value=question, inline=False), embed.add_field(name='Answer', value=random.choice(line))
        await ctx.send(embed=embed)
        
    @commands.command()
    async def sex(self, ctx, member: discord.Member):
        embed = discord.Embed(title = 'Haram Sex', description = f'{ctx.author.mention} just haram sexxed {member.mention} !!!')
        embed.set_image(url = "https://media1.tenor.com/images/ad6877ccbadd9584d9907a3caa0b01db/tenor.gif?itemid=15403668")
        await ctx.send(embed = embed)

    @sex.error
    async def sex_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Missing required argument!")
        else:
            raise error

def setup(bot):
    bot.add_cog(Misc(bot))
