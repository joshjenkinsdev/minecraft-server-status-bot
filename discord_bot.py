import os
import discord
from discord.ext import tasks
import socket
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MC_HOST = os.getenv("MC_HOST")
MC_PORT = int(os.getenv("MC_PORT"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def is_server_up(host, port, timeout=3):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False

@tasks.loop(seconds=45)
async def check_server():
    up = is_server_up(MC_HOST, MC_PORT)
    if up:
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Game(name="Server: Online")
        )
    else:
        await client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Game(name="Server: Offline")
        )

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    check_server.start()

client.run(DISCORD_TOKEN)