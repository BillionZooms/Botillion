import discord
from discord.ext import commands, tasks

from cogs.utilsb import users, sql, rooms, fields

import json
import logging
import os
import random


@tasks.loop(seconds=10)
async def refreshStats(cat):
    clist = cat.voice_channels
    for i in clist:
        guild = i.guild
        if i.name.startswith('Members'):
            count = users.countTrueMembers(guild)
            await i.edit(name = f'Members: {count}')
        elif i.name.startswith('Roles'):
            count = len(guild.roles)
            await i.edit(name = f'Roles: {count}')
        elif i.name.startswith('Channels'):
            count = 0
            for x in guild.channels:
                if not isinstance(x, discord.CategoryChannel):
                    count += 1
            await i.edit(name = f'Channels: {count}')
        elif i.name.startswith('Bots'):
            count = users.countBots(guild)
            await i.edit(name = f'Bots: {count}')

class Organize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def croom(self, ctx, user1, user2, *args):
        categories = ctx.guild.by_category()
        user1, user2 = await users.getUserFromMention(self.bot, user1), await users.getUserFromMention(self.bot, user2)
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
            puser = await users.getUserFromMention(self.bot, args[i])
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
            rooms.tempchannelAdd(str(ctx.author.id), vchannel.id)

    @commands.command()
    async def croom_clear(self, ctx):
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

    @commands.group()
    async def stats(self, ctx):
        if ctx.invoked_subcommand is None:
            categ = await sql.statsCategoryCheck(ctx.guild)
            if categ != False:
                embed = discord.Embed(title='Stats', color=15563278, description='This is the command to start configuring your stats category!')
                for i in categ.channels:
                    if i.name.lower().startswith("m"):
                        embed.add_field(name=i.name, value='Total members in server (excluding bots)', inline=False)
                    elif i.name.lower().startswith("r"):
                        embed.add_field(name=i.name, value='Total amount of roles in server', inline=False)
                    elif i.name.lower().startswith("b"):
                        embed.add_field(name=i.name, value='Total amount of channels in server', inline=False)
                    elif i.name.lower().startswith("c"):
                        embed.add_field(name=i.name, value='Total amount of bots in the server', inline=False)
                embed.add_field(name = 'Help', value = 'use **.stats help** for help.')
                await ctx.send(embed=embed)

            else:
                embed1 = discord.Embed(title='Stats', color=15563278, description='This is the command to start configuring your stats category!')
                fields.createFields(
                embed1, False,
                "Let's get started!", "Seems like you do not have a .stats category set up yet! To get started please create a category using **.stats category create**"
                )
                await ctx.send(embed=embed1)

    @stats.command(description = 'The stats help command.')
    async def help(self, ctx):
        embed = discord.Embed(title = 'Stats Help', description = 'The default help command for stats.', color = 15563278)
        for i in ctx.command.parent.commands:
            embed.add_field(name = i.name, value = i.description, inline = False)
        await ctx.send(embed = embed)


    @stats.command(description = 'Use this to create/remove/edit the stats category channel.')
    async def category(self, ctx, arg):
        overwritesVoice = {
                ctx.guild.default_role: discord.PermissionOverwrite(connect = False)
            }
        emlist = ['✨', '☁️', '💥', '🌈', '❌']
        if arg.lower() == 'create':
            if await sql.statsCategoryCheck(ctx.guild):
                return
            else:
                cat = await ctx.guild.create_category(name = 'STATS')
                await sql.statsAddCategory(cat)
                embed2 = discord.Embed(title='Setup', color=15563278, description="Nice! We're a step closer to having this all set up! Click the reactions below for which stats you want to add to your server! When you're done just press the ❌ reaction")
                fields.createFields(
                    embed2, False,
                    '✨: Members', 'Show total members in server (excluding bots)',
                    '☁️: Roles', 'Show total amount of roles in server',
                    '💥: Channels', 'Show total amount of channels in server',
                    '🌈: Bots', 'Show total amount of bots in the server'
                )
                msg = await ctx.send(embed=embed2)
            for emoji in emlist:
                await msg.add_reaction(emoji)
            while True:
                try:
                    def check(reaction, user):
                        if user == ctx.author:
                            for i in emlist:
                                if str(reaction.emoji) == i:
                                    return True
                            return False
                    reaction = await self.bot.wait_for('reaction_add', check = check, timeout = 60.0)
                except TimeoutError:
                    await ctx.send('Took too long to respond. Please restart by using **.stats** again')
                    return
                else:
                    count = 0
                    if str(reaction[0].emoji) == '✨':
                        x = 0
                        val = False
                        if not cat.voice_channels:
                            count = users.countTrueMembers(ctx.guild)
                            c1 = await cat.create_voice_channel(name = f'Members: {count}', overwrites=overwritesVoice)
                        else:
                            for x in cat.voice_channels:
                                if not 'Members' in x.name:
                                    continue
                                else:
                                    await c1.delete()
                                    val = True
                                    break
                            if val == False:
                                count = users.countTrueMembers(ctx.guild)
                                c1 = await cat.create_voice_channel(name = f'Members: {count}', overwrites=overwritesVoice)
                    elif str(reaction[0].emoji) == '☁️':
                        x = 0
                        val = False
                        if not cat.voice_channels:
                            count =  len(ctx.guild.roles)
                            c2 = await cat.create_voice_channel(name = f'Roles: {count}', overwrites=overwritesVoice)
                        else:
                            for x in cat.voice_channels:
                                if not 'Roles' in x.name:
                                    continue
                                else:
                                    await c2.delete()
                                    val = True
                                    break
                            if val == False:
                                count = len(ctx.guild.roles)
                                c2 = await cat.create_voice_channel(name = f'Roles: {count}', overwrites=overwritesVoice)
                    elif str(reaction[0].emoji) == '💥':
                        x = 0
                        val = False
                        if not cat.voice_channels:
                            count =  len(ctx.guild.channels)
                            c3 = await cat.create_voice_channel(name= f'Channels: {count}', overwrites=overwritesVoice)
                        else:
                            for x in cat.voice_channels:
                                if not 'Channels' in x.name:
                                    continue
                                else:
                                    await c3.delete()
                                    val = True
                                    break
                            if val == False:
                                count =  len(ctx.guild.channels)
                                c3 = await cat.create_voice_channel(name= f'Channels: {count}', overwrites=overwritesVoice)
                    elif str(reaction[0].emoji) == '🌈':
                        x = 0
                        val = False
                        if not cat.voice_channels:
                            count = users.countBots(ctx.guild)
                            c4 = await cat.create_voice_channel(name = f'Bots: {count}', overwrites=overwritesVoice)
                        else:
                            for x in cat.voice_channels:
                                if not 'Bots' in x.name:
                                    continue
                                else:
                                    await c4.delete()
                                    val = True
                                    break
                            if val == False:
                                count = users.countBots(ctx.guild)
                                c4 = await cat.create_voice_channel(name = f'Bots: {count}', overwrites=overwritesVoice)
                    else:
                        if not cat.voice_channels:
                            await cat.delete()
                            return
                        else:
                            refreshStats.start(cat)
                            await msg.delete()
                            return


def setup(bot):
    bot.add_cog(Organize(bot))