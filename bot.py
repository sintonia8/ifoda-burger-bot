import os
import discord
from groq import Groq

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

CANAL_PERMITIDO = 1535432413075869766

@client.event
async def on_ready():
    print(f"O BALCÃO DO I-FODA BURGER TA ABERTO, PORRA! 🍔🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel) and message.channel.id != CANAL_PERMITIDO:
        return

    if isinstance(message.channel, discord.DMChannel) or client.user.mentioned_in(message) or any(k in message.content.lower() for k in ["pedido", "atendente", "lanche"]):
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        mensagens = [
            {"role": "system", "content": "Voce e o atendente mais escroto e puto do I-Foda Burger. XINGUE PRA CARALHO, solte muito palavrao a cada frase (porra, caralho, desgraca, arrombado, fdp). Aceite qualquer prato bizarro que o cliente inventar, cobre uma fortuna absurda, mande se foder e use asteriscos p/ acoes (*joga o troco na tua cara*, *grita pra chapa*). SEM NEGRITO. Maximo 2 frases curtas. Mande essa desgraca pedir logo.FALE POUCO"}
        ]
        
        if not prompt:
            prompt = "Fala logo o q tu quer, porra."

        mensagens.append({"role": "user", "content": prompt})

        try:
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensagens,
                max_tokens=167,
                temperature=1.0
            )
            await message.channel.send(chat_completion.choices[0].message.content)
        except Exception as e:
            await message.channel.send("A chapa explodiu nessa porra! Vaza!")

token = os.getenv("DISCORD_TOKEN")
client.run(token)
