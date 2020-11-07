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
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(line)}')



def setup(bot):
    bot.add_cog(Misc(bot))
