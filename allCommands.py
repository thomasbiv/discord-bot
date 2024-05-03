import discord
from discord.ext.commands import bot
from discord.ext import commands

class allCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(name="ping")
    async def ping(self, ctx):
        await ctx.send(f'Pong! :ping_pong: - {round(self.bot.latency * 1000)}ms')

def setup(bot):
    bot.add_cog(allCommands(bot))