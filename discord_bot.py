import os
import discord
from discord.ext import tasks
from mcstatus import JavaServer
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
MC_HOST = os.getenv("MC_HOST")
MC_PORT = int(os.getenv("MC_PORT"))

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def get_server_status(host, port):
    try:
        server = JavaServer.lookup(f"{host}:{port}")
        status = server.status()
        return True, status.players.online, status.players.max
    except Exception:
        return False, 0, 0

@tasks.loop(seconds=45)
async def check_server():
    up, online, max_players = get_server_status(MC_HOST, MC_PORT)
    if up:
        text = f"{online}/{max_players} online"
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(type=discord.ActivityType.watching, name=text)
        )
    else:
        await client.change_presence(
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.watching, name="Server Offline")
        )

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    check_server.start()

client.run(DISCORD_TOKEN)