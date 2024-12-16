import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import importlib

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="!", intents=discord.Intents.default())


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        await load_cogs()
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(f"Error syncing commands: {e}")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if (
            filename.endswith(".py")
            and filename != "__init__.py"
            and filename != "utils.py"
        ):
            cog_name = filename[:-3]
            try:
                importlib.import_module(f"cogs.{cog_name}")
                await client.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")


if __name__ == "__main__":
    client.run(TOKEN)
