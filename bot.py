import os
import asyncio  
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp

load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # <--- Vital para que lea los comandos
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuración de yt-dlp para extraer el link de audio de YouTube
ytdl_format_options = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    # Esto evita el error de "Sign in to confirm you're not a bot"
    'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
}

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

@bot.event
async def on_ready():
    print(f"¡El bot {bot.user.name} está conectado y listo para poner música en la PS1!")

@bot.command(name="unir")
async def unirse(ctx):
    """Comando para que el bot entre al canal de voz"""
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is not None:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"🎧 ¡Aku Aku se ha unido a **{channel.name}**!")
    else:
        await ctx.send("❌ ¡Tienes que estar conectado a un canal de voz primero, bandicoot!")

@bot.command(name="play")
async def reproducir(ctx, *, query):
    """Comando para reproducir música con !play"""
    
    # 1. Verificar si el usuario está en un canal de voz
    if not ctx.author.voice:
        await ctx.send("❌ ¡Tienes que estar conectado a un canal de voz primero, bandicoot!")
        return

    channel = ctx.author.voice.channel

    # 2. Si el bot no está conectado, se une automáticamente al canal del usuario
    if ctx.voice_client is None:
        try:
            await channel.connect()
        except Exception as e:
            await ctx.send(f"❌ No pude conectarme al canal de voz: {e}")
            return
    elif ctx.voice_client.channel != channel:
        # Si está en otro canal, se mueve al tuyo
        await ctx.voice_client.move_to(channel)

    async with ctx.typing():
        try:
            # 3. Buscar y reproducir la pista
            player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
            
            # Verificamos una vez más que el cliente de voz esté activo
            if ctx.voice_client is None:
                await ctx.send("❌ Error: El bot perdió la conexión de voz.")
                return

            ctx.voice_client.play(player, after=lambda e: print(f'Error en el reproductor: {e}') if e else None)
            await ctx.send(f"🎶 Aku Aku está sonando: **{player.title}**")
            
        except Exception as e:
            await ctx.send(f"❌ Ocurrió un error al intentar reproducir la música: {e}")
            
@bot.command(name="salir")
async def salir(ctx):
    """Comando para sacar al bot del canal de voz"""
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("👋 ¡Aku Aku se retira del canal de audio!")
    else:
        await ctx.send("❌ ¡No estoy en ningún canal de voz!")

# Arrancar el bot con el token configurado
bot.run(TOKEN)