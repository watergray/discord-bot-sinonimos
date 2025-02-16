import discord
import requests
import asyncio
from discord.ext import tasks

# Reemplaza con tu token
TOKEN = 'TU_TOKEN_AQUI'

# Canal donde el bot enviará los mensajes
CHANNEL_ID = 123456789012345678  # Reemplaza con el ID del canal

intents = discord.Intents.default()
client = discord.Client(intents=intents)

def obtener_sinonimo_aleatorio():
    url = "https://api.datamuse.com/words?rel_syn=happy"  # Puedes cambiar "happy" por otra palabra
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            palabra = data[0]['word']
            significado = "Aquí podrías obtener el significado de la palabra usando otra API o un diccionario."
            return palabra, significado
    return None, None

@tasks.loop(hours=2)
async def enviar_sinonimo():
    channel = client.get_channel(CHANNEL_ID)
    palabra, significado = obtener_sinonimo_aleatorio()
    if palabra and significado:
        await channel.send(f"Palabra: {palabra}\nSignificado: {significado}")
    else:
        await channel.send("No se pudo obtener un sinónimo en este momento.")

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    enviar_sinonimo.start()

client.run(TOKEN)
