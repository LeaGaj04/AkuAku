import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import yt_dlp

# Cargar variables de entorno (si usas localmente o en Railway)
load_dotenv()
TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Configuración de yt-dlp para extraer el link de audio de YouTube
ytdl_format_options = {
    'format': 'bestaudio/best',
    'nostream': True,
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
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
    """Comando para reproducir música escribiendo !play [nombre o link de YouTube]"""
    if not ctx.voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("❌ ¡Tienes que estar en un canal de voz para que pueda poner música!")
            return

    async with ctx.typing():
        try:
            # Buscar y preparar la pista de audio
            player = await YTDLSource.from_url(query, loop=bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print(f'Error en el reproductor: {e}') if e else None)
            await ctx.send(f"🎶 Reproduciendo ahora mismo: **{player.title}**")
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