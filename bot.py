import os
import discord
from groq import Groq

# Inicializa o cliente
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"O BALCÃO DO I-FODA BURGER ESTÁ ABERTO, CARALHO! 🍔🔥")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # No fast food, se o cara falar qualquer coisa ou marcar o bot, o atendente já atende no grito
    if isinstance(message.channel, discord.DMChannel) or client.user.mentioned_in(message) or "pedido" in message.content.lower() or "atendente" in message.content.lower() or "lanche" in message.content.lower():
        prompt = message.content.replace(f"<@{client.user.id}>", "").strip()
        
        # System Prompt do Atendente de Fast Food Encapetado
        mensagens = [
            {"role": "system", "content": "Você é o atendente do 'I-Foda Burger', a lanchonete mais caótica e estressada do multiverso. O atendimento é estilo fast food: agressivo, impaciente, mandando o cliente decidir logo o pedido, inventando lanches absurdos e fictícios (tipo 'X-Morte com radiação', 'Batata frita atômica com poção de lentidão') e cobrando caro. Usa gírias de carioca, xinga de leve (crlh, porra, desgraça), faz RP de atendente jogando o troco na cara ou gritando pro cozinheiro na chapa entre asteriscos (*grita pra cozinha*). NUNCA USE NEGRITO. Seja curto (máximo 3 linhas), mantenha a resenha pesada e exija o pedido do cliente imediatamente."}
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
