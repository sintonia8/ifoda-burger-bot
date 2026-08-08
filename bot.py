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
    print(f"O BALCÃO DO I-FODA BURGER TÁ ABERTO, PORRA!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # SÓ RESPONDE NO CANAL CERTO OU DM, E SEMPRE RESPONDE (SEM GATILHO)
    if not isinstance(message.channel, discord.DMChannel) and message.channel.id != CANAL_PERMITIDO:
        return

    # Manda a mensagem limpa pro prompt
    prompt = message.content.strip()
    
    mensagens = [
        {"role": "system", "content": "Voce e o atendente do I-Foda Burger. Fale direto, como se estivesse conversando comigo cara a cara. NUNCA escreva 'atendente:' ou 'cliente:'. NUNCA use negrito. Use muitos palavroes (porra, caralho, arrombado, fdp). Seja curto, agressivo e mande o cliente logo pro inferno. Aceite qualquer pedido absurdo e cobre caro."}
    ]
    
    mensagens.append({"role": "user", "content": prompt})

    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=mensagens,
            max_tokens=80, # Token baixo pra ser curto e grosso
            temperature=1.0
        )
        await message.channel.send(chat_completion.choices[0].message.content)
    except Exception as e:
        await message.channel.send("A chapa explodiu nessa porra, espera caralho!")

token = os.getenv("DISCORD_TOKEN")
client.run(token)
