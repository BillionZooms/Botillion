from discord.ext import commands

def createFields(embed, inline, *args ):
    for x in range(0, len(args), 2):
        try:
            embed.add_field(name=args[x], value=args[x+1], inline=inline)
        except Exception as xx:
            print(xx)
            break
