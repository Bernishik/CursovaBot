import json

import telebot
from flask import Flask, request
from telebot import types

import config
from Rozk import Rozk
from Users import Users

rozklad = Rozk()
users = Users()
bot = telebot.TeleBot(config.TOKEN)  # You can set parse_mode by default. HTML or MARKDOWN

app = Flask(__name__)
bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL_BASE)
print(bot.get_webhook_info())



def group_config(message,txt=None):
    if txt is not None:
        bot.send_message(message.chat.id, text=txt)
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("1", callback_data='1kurs')
    item2 = types.InlineKeyboardButton("2", callback_data='2kurs')
    item3 = types.InlineKeyboardButton("3", callback_data='3kurs')
    item4 = types.InlineKeyboardButton("4", callback_data='4kurs')
    item5 = types.InlineKeyboardButton("5", callback_data='5kurs')
    item6 = types.InlineKeyboardButton("6", callback_data='6kurs')
    markup.add(item1, item2, item3, item4, item5,item6)
    bot.send_message(message.chat.id, "Оберіть курс:", reply_markup=markup)

def get_started(message):
    keyboard1 = types.ReplyKeyboardMarkup(True, True)
    button1 = types.KeyboardButton("Розклад")
    button2 = types.KeyboardButton("Налаштування")
    keyboard1.add(button1)
    keyboard1.add(button2)
    bot.send_message(message.chat.id, "Ви успішно обрали групу,тепер можете дивитися розклад натискаючи на кнопку справа",reply_markup=keyboard1)


@bot.message_handler(commands=['start'])
def start_message(message):
    if message.chat.type == 'private':
        bot.send_message(message.chat.id,"Привіт")
        group_config(message)


        # bot.send_message(message.chat.id, 'Здоровенькі були,  сподіваюсь комусь пригодиться)', reply_markup=keyboard1)



@bot.message_handler(func=lambda message: True, content_types=['text'])
def rozk_message(message):
    # bot.reply_to(message, message.text)
    if message.chat.type == 'private':
        if message.text == "Розклад":
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Понеділок", callback_data='Понеділок')
            item2 = types.InlineKeyboardButton("Вівторок", callback_data='Вівторок')
            item3 = types.InlineKeyboardButton("Середа", callback_data='Середа')
            item4 = types.InlineKeyboardButton("Четвер", callback_data='Четвер')
            item5 = types.InlineKeyboardButton("Пятниця", callback_data='Пятниця')

            markup.add(item1, item2, item3, item4, item5)
            bot.send_message(message.chat.id, "Оберіть день:", reply_markup=markup)
        elif message.text == "Налаштування":
            group_config(message,"Оберіть нові налаштування групи")

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        chat_id = int(call.message.chat.id)

    except Exception as e:
        print(e)
    if call.data == 'Понеділок' or call.data == 'Вівторок' or call.data == 'Середа' or call.data == 'Четвер' or call.data == 'Пятниця':
        try:
            user =users.get_user_by_chat_id(chat_id)["group"]
            group = user["group"] + str(user["kurs"]) + str(user["group_num"]) + "-" + str(user["subgroup"])
            path = rozklad.get_day_rozk(group, call.data)
            try:
                bot.send_photo(call.message.chat.id, photo=open(path, 'rb'))
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, "Виникла помилка, звяжіться з адміністратором")
        except TypeError:
            bot.send_message(call.message.chat.id, "Будь-ласка виберіть групу:")
            group_config(call.message)


    if call.data == "1kurs" or call.data == "2kurs" or call.data == "3kurs" or call.data == "4kurs" or call.data == "5kurs" or call.data == "6kurs":
        kurs = int(call.data[0])
        groups = rozklad.get_group_list_by_kurs(kurs)
        markup = types.InlineKeyboardMarkup(row_width=2)
        items = []
        for group in groups:
            g =types.InlineKeyboardButton(group["group"], callback_data=group["group"] + str(kurs))
            items.append(g)

        if items:
            markup.add(*items)
            bot.send_message(call.message.chat.id, "Оберіть потік:", reply_markup=markup)
        else:
            group_config(call.message,"Нажаль на даний момент немає груп для даного курсу в боті. Зверніться до адміна бота")


    if call.data[:-1] in [x["group"] for  x in rozklad.get_group_list()] :
        kurs = int(call.data[-1])
        groups = rozklad.get_group_list_by_kurs(kurs)
        markup = types.InlineKeyboardMarkup(row_width=2)
        items = []
        for group in groups:
            g = types.InlineKeyboardButton(group["group"]+str(group["kurs"])+str(group["group_num"])+"-"+str(group["subgroup"]), callback_data=json.dumps(group))
            items.append(g)

        if items:
            markup.add(*items)
            bot.send_message(call.message.chat.id, "Оберіть групу:", reply_markup=markup)
        else:
            bot.send_message(call.message.chat.id,
                     "Нажаль на даний момент немає потоку для даного потоку в боті. Зверніться до адміна бота" )
            group_config(call.message)

    try:
        if json.loads(call.data) in rozklad.get_group_list():
            data = json.loads(call.data)

            users.add_user(call.message.chat.id,data,call.from_user.username,call.from_user.id,
                           call.from_user.language_code,call.message.date)
            get_started(call.message)
    except ValueError:
        pass

@app.route('/', methods=['POST', 'GET'])
def getMessage():
    msg = request.stream.read().decode("utf-8")
    print(msg)
    bot.process_new_updates([telebot.types.Update.de_json(msg)])
    return "!", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(config.FLASK_PORT))

# bot.polling()
