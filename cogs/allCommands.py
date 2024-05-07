import discord
import settings
from discord.ext.commands import bot
from discord.ext import commands

logger = settings.logging.getLogger("bot")

class allCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        logger.info(f"Ping. Sent by: {ctx.message.author}")
        await ctx.send(f'Pong! :ping_pong: - {round(self.bot.latency * 1000)}ms')
        
async def setup(bot):
    await bot.add_cog(allCommands(bot))