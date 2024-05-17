import asyncio
import settings
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions

from asyncio import sleep
from discord.utils import get

logger = settings.logging.getLogger("bot")

class allCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help="Shows the ping/latency of the bot in miliseconds. Format: '$ping'",
        brief="Format: $ping"
    )
    async def ping(self, ctx):
        logger.info(f"Ping. Sent by: {ctx.message.author}")
        await ctx.send(f'Pong! :ping_pong: - {round(self.bot.latency * 1000)}ms')

    @commands.command(
        help="Allows user to create a poll with up to 10 options, seperated by commas. Format: '$poll [title], [time (mins)], [option1], [option2],...[option10]." + 
                "\nPoll results display after specified amount of time.",
        brief="Format: $poll [title], [time (mins)], [option1], [option2],...[option10]"
    )
    async def poll(self, ctx, *, message):
        #---VOTING PHASE---#
        await ctx.channel.purge(limit=1)
        messagelist = [x.strip() for x in message.split(',')]
        if len(messagelist) > 12:
            embed=discord.Embed(title = "***" + "Poll contains too many options!" + "***")
            embed.add_field(name = "", value = "The limit is 10 choices. Please try again.", inline=False)
            return await ctx.send(embed=embed)
        if messagelist[1].isdigit() == False:
            embed=discord.Embed(title = "***" + "Poll time invalid!" + "***")
            embed.add_field(name = "", value = "The poll time in minutes must be expressed as a number. Please try again.", inline=False)
            return await ctx.send(embed=embed)
        if len(messagelist) < 3:
            embed=discord.Embed(title = "***" + "Missing arguments!" + "***")
            embed.add_field(name = "", value = "You are missing some required arguments for this command. Please try again.", inline=False)
            return await ctx.send(embed=embed)
        embed=discord.Embed(title = "***" + messagelist[0] + "***")
        numbers_to_words = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        for i in range(len(messagelist)):
            if i > 1:
                embed.add_field(name = "", value = numbers_to_words[i - 2] + " " + messagelist[i], inline=False)
        msg = await ctx.send(embed=embed)
        for j in range(len(messagelist)):
            if j > 1:
                await msg.add_reaction(numbers_to_words[j - 2])

        await sleep(int(messagelist[1]) * 60) #Voting phase length is now determined by user input

        #---RESULTS PHASE---#
        refreshed_msg = await ctx.fetch_message(msg.id)
        reactions_array = refreshed_msg.reactions
        #await ctx.channel.purge(limit=1) May add this back, may want to clean up as to not see the old poll after results post
        embed=discord.Embed(title = "***" + "Poll results final!" + "***")
        embed.add_field(name = "", value = "Poll: " + messagelist[0], inline=False)
        embed.add_field(name = "", value = "Here are the results:", inline=False)
        for entry in range(len(reactions_array)):
            embed.add_field(name = "", value = reactions_array[entry].emoji + " " + messagelist[entry + 2] + " --> " + str(reactions_array[entry].count - 1), inline=False)
        results_msg = await ctx.send(embed=embed)

    @commands.command(
        help="Allows users to delete a specified amount of messages (up to 100) in the current chat (default = 1). Format: '$purge [amount]'",
        brief="Max: 100 - Format: $purge [amount]"
    )
    @commands.has_permissions(administrator = True)
    async def purge(self, ctx, amount=1):

        if(amount > 100):
            await ctx.send("The maximum amount of messages you can purge is 100!")
            return

        await ctx.send("Are you sure you want to purge " + str(amount) + " messages? (yes/no)")

        def check(m): # checking that confirmation is from the same user in the same channel
            return m.author == ctx.author and m.channel == ctx.channel

        try: # waiting for message
            response = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            return

        # if response is different than yes / y - return
        if response.content.lower() not in ("yes", "y"): # lower() makes everything lowercase to also catch: YeS, YES etc.
            return

        await ctx.channel.purge(limit=amount+3)
        
async def setup(bot):
    await bot.add_cog(allCommands(bot))