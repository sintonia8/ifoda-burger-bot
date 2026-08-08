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
    print(f"O BALCÃO DO I-FODA BURGER TA ATIVO, PORRA!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not isinstance(message.channel, discord.DMChannel) and message.channel.id != CANAL_PERMITIDO:
        return

    prompt = message.content.strip()
    
    mensagens = [
        {"role": "system", "content": "Voce e uma pessoa real atendendo no balcao do I-Foda Burger, nao um robo. Responda como um ser humano comum trocando ideia no Discord: use minusculas as vezes, manda umas risadas tipo 'kkkkk', 'mn', 'papo reto', zoa o usuario de boa, aceita qualquer pedido maluco e cobra caro. Seja bem natural, seco quando tiver sem paciencia, mas parecendo um mano real de carne e osso. Sem roteiros, sem negrito, maximo 2 frases curtas."}
    ]
    
    mensagens.append({"role": "user", "content": prompt})

    try:
        chat_completion = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=mensagens,
            max_tokens=40,
            temperature=1.0
        )
        await message.channel.send(chat_completion.choices[0].message.content)
    except Exception as e:
        await message.channel.send("pera ai que a chapa travou aqui")

token = os.getenv("DISCORD_TOKEN")
client.run(token)
