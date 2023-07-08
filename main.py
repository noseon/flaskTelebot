# -*- coding: utf-8 -*-

import logging
import os
from flask import Flask, request
import telebot


#################
import openai
	
openai.api_key = os.getenv("OPENAI_API_KEY") 

chat_language = os.getenv("INIT_LANGUAGE", default="zh") #altere aqui para mudar seu idioma predefinido
	
conversation = []

class ChatGPT:  
    def __init__(self):
        self.messages = conversation
        self.model = os.getenv("OPENAI_MODEL", default="gpt-3.5-turbo")

    def get_response(self, user_input):
        conversation.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages
        )
        conversation.append({"role": "assistant", "content": response['choices'][0]['message']['content']})
        print("Conteúdo da resposta da IA:")
        print(response['choices'][0]['message']['content'].strip())
        return response['choices'][0]['message']['content'].strip()

#####################

telegram_bot_token = str(os.getenv("6294585980:AAH8WFD-CbbMfV6ZEtYV36m58qPGHvQTxjY"))

# Load data from config.ini file
#config = configparser.ConfigParser()
#config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
app = Flask(__name__)

# Initial bot by Telegram access token
bot = telebot.TeleBot(telegram_bot_token)


@app.route('/callback', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telebot.types.Update.de_json(request.get_json(force=True), bot)

        # Update bot with received update
        bot.process_new_updates([update])
    return 'ok'


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Olá! Estou aqui para ajudar. Envie-me uma mensagem.")

@bot.message_handler(func=lambda message: True)
def reply_handler(message):
    chatgpt = ChatGPT()
    ai_reply_response = chatgpt.get_response(message.text)
    bot.reply_to(message, ai_reply_response)

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
