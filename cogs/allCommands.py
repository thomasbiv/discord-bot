import settings
import discord
from discord.ext import commands

from asyncio import sleep
from discord.utils import get

logger = settings.logging.getLogger("bot")

class allCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Shows the ping/latency of the bot in miliseconds.",
        brief="Shows ping."
    )
    async def ping(self, ctx):
        logger.info(f"Ping. Sent by: {ctx.message.author}")
        await ctx.send(f'Pong! :ping_pong: - {round(self.bot.latency * 1000)}ms')

    @commands.command(
        help="Allows user to create a poll with up to 10 options, seperated by commas. Format: '$poll [title], [option1], [option2],...[option10]." + 
                "\nPoll results display after 1 minute.",
        brief="Format: '$poll [title], [option1], [option2],...[option10]"
    )
    async def poll(self, ctx, *, message):
        #---VOTING PHASE---#
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

        await sleep(60) #Allow one minute for voting phase, plan to add input for user to determine voting time

        #---LOADING PHASE---#
        #await ctx.channel.purge(limit=1) <----- May add this back, may want to clean up as to not see the old poll after results post
        embed=discord.Embed(title = "***" + "Poll results final!" + "***")
        embed.add_field(name = "", value = "Poll: " + messagelist[0], inline=False)
        embed.add_field(name = "", value = "Here are the results:", inline=False)
        embed.add_field(name = "", value = "Loading...", inline=False)
        temp = await ctx.send(embed=embed)

        await sleep(3) #Allow short pause to allow bot to retrieve reactions on poll

        #---RESULTS PHASE---#
        refreshed_msg = await ctx.fetch_message(msg.id)
        reactions_array = refreshed_msg.reactions
        await ctx.channel.purge(limit=1)
        embed=discord.Embed(title = "***" + "Poll results final!" + "***")
        embed.add_field(name = "", value = "Poll: " + messagelist[0], inline=False)
        embed.add_field(name = "", value = "Here are the results:", inline=False)
        for entry in range(len(reactions_array)):
            embed.add_field(name = "", value = reactions_array[entry].emoji + " " + messagelist[entry + 1] + " --> " + str(reactions_array[entry].count - 1), inline=False)
        results_msg = await ctx.send(embed=embed)
        
async def setup(bot):
    await bot.add_cog(allCommands(bot))