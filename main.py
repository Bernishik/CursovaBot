import telebot
from flask import Flask, request
import config


bot = telebot.TeleBot(config.TOKEN)  # You can set parse_mode by default. HTML or MARKDOWN

app = Flask(__name__)
bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL_BASE)
print(bot.get_webhook_info())


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@app.route('/', methods=['POST', 'GET'])
def getMessage():
    msg = request.stream.read().decode("utf-8")
    print(msg)
    bot.process_new_updates([telebot.types.Update.de_json(msg)])
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(config.FLASK_PORT))

# bot.polling()
