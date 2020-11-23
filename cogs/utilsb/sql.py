import aiosqlite
import discord
from discord.ext import commands, tasks

sqldb = """CREATE TABLE IF NOT EXISTS stats (
            guildID INT PRIMARY KEY,
            categoryID INT,
            members INT,
            roles INT,
            bots INT
        )"""


async def statsAddCategory(cat):
    async with aiosqlite.connect('org.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""INSERT INTO stats (guildID, categoryID) VALUES (:guildID, :categoryid)""", {'guildID': cat.guild.id, 'categoryid': cat.id})
            await db.commit()
    
async def statsCategoryCheck(guild):
    async with aiosqlite.connect('org.db') as db:
        await db.execute(sqldb)
        async with db.cursor() as crs:
            await crs.execute("""SELECT guildID, categoryID FROM stats""")
            vals = await crs.fetchall()  
            for i in vals:
                if guild.id == i[0]:    
                    for channels in guild.categories:
                        if channels.id == i[1]:
                            return channels
                    await crs.execute("""DELETE from stats where guildID = :guildID""", {'guildID': guild.id})
                    await db.commit()
                    return False
                            
        return False            
