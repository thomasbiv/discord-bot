import settings
import discord
from discord.ext import commands

logger = settings.logging.getLogger("bot")

def run():
    intents = discord.Intents.default() #<-- May change this to all() instead of default later depending on what we want
    bot = commands.Bot(command_prefix="$", intents = intents)
    
    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        # Initial testing strings, since replaced with logging:
        # print(bot.user)
        # print(bot.user.id)
        # print("------------")
        # print("Initialized.")
    
    bot.run(settings.DISCORD_API_SECRET)

if __name__ == "__main__":
    run()
