import os
import discord
from groq import Groq

# Inicializa o cliente
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# CANAL ESPECÍFICO JÁ CONFIGURADO
CANAL_PERMITIDO = 1535432413075869766

@client.event
async def on_ready():
    print(f"O BALCÃO DO I-FODA BURGER ESTÁ ABERTO, CARALHO! 🍔🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # SE O CANAL NÃO FOR O PERMITIDO E NÃO FOR DM, ELE IGNORA COMPLETAMENTE
    if not isinstance(message.channel, discord.DMChannel) and message.channel.id != CANAL_PERMITIDO:
        return

    # Atendimento normal no canal liberado ou na DM
    if isinstance(message.channel, discord.DMChannel) or client.user.mentioned_in(message) or "pedido" in message.content.lower() or "atendente" in message.content.lower() or "lanche" in message.content.lower():
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        mensagens = [
            {"role": "system", "content": "Você é o atendente mais resenhudo e folgado do 'I-Foda Burger'. O cliente pode pedir QUALQUER LANCE ABSURDO ou fictício, e tu és OBRIGADO a aceitar, inventando os ingredientes mais bizarros possíveis na hora (tipo lama de vulcão, unha de gato intergaláctico, poção de invisibilidade) e cobrando uma fortuna em dinheiro ou órgãos. Usa gírias de carioca pesadas, xinga de leve (crlh, porra, desgraça), faz RP jogando o troco na cara ou gritando pro cozinheiro na chapa (*grita pra cozinha*). NUNCA USE NEGRITO. Seja curto (máximo 3 linhas), mantenha a resenha caótica e esculacha o cliente com estilo."}
        ]
        
        if not prompt:
            prompt = "Oi, quero ser atendido."

        mensagens.append({"role": "user", "content": prompt})

        try:
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=mensagens,
                max_tokens=200,
                temperature=0.9
            )
            await message.channel.send(chat_completion.choices[0].message.content)
        except Exception as e:
            await message.channel.send("A chapa explodiu aqui, caralho! Volta daqui a pouco!")

token = os.getenv("DISCORD_TOKEN")
client.run(token)
