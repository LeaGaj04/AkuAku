import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carga las variables secretas del archivo .env
load_dotenv()

# Lee el token de forma segura desde el sistema
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"¡El bot {bot.user.name} está conectado y seguro con variables de entorno!")

@bot.command(name="unir")
async def unirse(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎧 ¡Conectado al canal: **{channel.name}**!")
    else:
        await ctx.send("❌ ¡Conéctate a un canal de voz primero!")

@bot.command(name="salir")
async def salir(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ¡Desconectado!")
    else:
        await ctx.send("❌ ¡No estoy en ningún canal!")

# Arranca el bot usando la variable segura
bot.run(TOKEN)