import discord
from discord.ext.commands import bot
from discord.ext import commands

class allCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! :ping_pong: - {round(self.bot.latency * 1000)}ms')

    @commands.command()
    async def poll(self, ctx, *, message):
        await ctx.channel.purge(limit=1)
        messagelist = [x.strip() for x in message.split(',')]
        if len(messagelist) > 11:
            embed=discord.Embed(title = "***" + "Poll contains too many options!" + "***")
            embed.add_field(name = "", value = "The limit is 10 choices. Please try again.", inline=False)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title = "***" + messagelist[0] + "***")
        numbers_to_words = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for i in range(len(messagelist)):
            if i > 0:
                embed.add_field(name = "", value = numbers_to_words[i] + " " + messagelist[i], inline=False)
        msg = await ctx.send(embed=embed)
        for j in range(len(messagelist)):
            if j > 0:
                await msg.add_reaction(numbers_to_words[j])
        
def setup(bot):
    bot.add_cog(allCommands(bot))