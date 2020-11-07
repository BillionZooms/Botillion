import discord
from discord.ext import commands

from cogs.utilsb import users
from cogs.utilsb import rooms

import json
import logging
import os
import random




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



def setup(bot):
    bot.add_cog(Organize(bot))