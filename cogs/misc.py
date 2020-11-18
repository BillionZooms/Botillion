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
        
def setup(bot):
    bot.add_cog(Misc(bot))
