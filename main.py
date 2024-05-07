import settings
import discord
from discord.ext import commands
import os
import asyncio

logger = settings.logging.getLogger("bot")

intents = discord.Intents.all() #<-- May change this to all() instead of default later depending on what we want
intents.members = True
bot = commands.Bot(command_prefix="$", intents = intents)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()

    @bot.event
    async def on_ready():
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
    
        if message.content.startswith("$"):
            await message.add_reaction("👍")
        await bot.process_commands(message)
    
    await bot.start(settings.DISCORD_API_SECRET)


if __name__ == "__main__":
    asyncio.run(main())
