import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix= 'cum.')



@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ['It is certain',
             'Without a doubt',
             'You may rely on it',
             'Yes definitely',
             'It is decidedly so',
             'As I see it, yes',
             'Most likely',
             'Yes',
             'Outlook good',
             'Signs point to yes',
             'Reply hazy try again',
             'Better not tell you now',
             'Ask again later',
             'Cannot predict now',
             'Concentrate and ask again',
             'Don’t count on it',
             'Outlook not so good',
             'My sources say no',
             'Very doubtful',
             'My reply is no']
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')
    



client.run('Njk1NjA4OTM3NTAzOTE2MDMy.XocqTg.dLy9yrpUYKgOQZ4M4hWKsAlgGl0')