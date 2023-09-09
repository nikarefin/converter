import telebot
from config import TOKEN, currencies
from extensions import APIException, Convertion


bot = telebot.TeleBot(TOKEN, parse_mode='markdown')


@bot.message_handler(commands=['start', 'help'])
def greeting(message):
    bot.send_message(message.chat.id, 'Для конвертирования напишите через '
                                      'пробел:\n'
                                      '- валюту, которую конвертируем\n'
                                      '- в какую валюту конвертируем\n'
                                      '- количество валюты\n\n'
                                      'Пример запроса:\n'
                                      '*доллар рубль 100*\n\n'
                                      'Доступные валюты: /values')


@bot.message_handler(commands=['values'])
def show_values(message):
    text = '*Доступные валюты:*'
    for currency in currencies.values():
        text = f'{text}\n{currency[1]}'
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Должно быть 3 параметра')

        base, quote, amount = values
        total_base, base_unit, quote_unit = Convertion.get_price(base, quote, amount)

    except APIException as e:
        bot.reply_to(message, f'*Ошибка пользователя*\n{e}')
    except Exception as e:
        bot.reply_to(message, f'*Не удалось обработать команду*\n{e}')
    else:
        total = float(total_base) * float(amount)
        total = Convertion.pretty_number(total, 'float')
        amount = Convertion.pretty_number(amount, 'int')

        text = f'*{amount}* {base_unit} = *{total}* {quote_unit}'
        bot.send_message(message.chat.id, text)


bot.polling()
