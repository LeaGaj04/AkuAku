import discord
from discord.ext import commands

# Configurar los intents del bot
intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

# Crear la instancia del bot (puedes cambiar el prefijo '!' por el que prefieras)
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"¡El bot {bot.user.name} está conectado al Laboratorio y listo en la PS1!")

@bot.command(name="unir")
async def unirse(ctx):
    """Comando para que el bot entre al canal de voz donde estás"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎧 ¡Conectado al canal de voz: **{channel.name}**!")
    else:
        await ctx.send("❌ ¡Tienes que estar conectado a un canal de voz primero, bandicoot!")

@bot.command(name="salir")
async def salir(ctx):
    """Comando para sacar al bot del canal de voz"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ¡Desconectado del canal de audio!")
    else:
        await ctx.send("❌ ¡No estoy en ningún canal de voz!")

# PEGA TU TOKEN SECRETO ENTRE LAS COMILLAS ABAJO
bot.run("MTU1OTk3NTY5MjU5NzIwNzA3Mw.Grg1HL.ix7hgl2qALCrIqb3AlsIEJv-8VzVVSOQ1crvKY")