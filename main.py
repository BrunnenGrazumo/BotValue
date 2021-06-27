from config import TOKEN, exchanger
import telebot
from extensions import Convertor, ConverterException

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    cmd = message.text
    hello = 'Вас приветсвует бот конвертации валюты.\n'
    instructions = 'Для работы с ботом введите текст в следующем формате через пробел:\n1.название изначальной валюты  \
\n2.название валюты в которую нужно конвертировать \n3.количество валюты. \nСписок валют: /values'
    if cmd == '/start':
        bot.send_message(message.chat.id, hello + instructions)

    if cmd == '/help':
        bot.send_message(message.chat.id, instructions)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = '*Доступные валюты:\n*'
    text += '\n'.join(f'{i + 1}. {key}' for i, key in enumerate(exchanger.keys()))
    bot.send_message(message.chat.id, text, parse_mode='Markdown')


@bot.message_handler(content_types='text')
def converter(message: telebot.types.Message):
    values = message.text.split()
    values = list(map(str.lower, values))

    try:
        result = Convertor.get_price(values)
        print(result)
    except ConverterException as e:
        bot.send_message(message.chat.id, e)
    except Exception as e:
        bot.send_message(message.chat.id, f'Ошибка программы:\n{e}')
    else:
        text = f'{values[2]} {result[1]} = {result[0]} {result[2]}'
        bot.send_message(message.chat.id, text)


bot.polling()
