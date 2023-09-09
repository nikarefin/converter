import requests
import json
from config import currencies


class APIException(Exception):
    pass


class Convertion:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        base = base.lower()
        quote = quote.lower()
        right_base = None
        right_quote = None

        if base == quote:
            raise APIException('Валюты должны быть разные')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException('Количество должно быть числом')

        for currency in currencies:
            if currencies[currency][0] in base:
                base = currency
                base_unit = currencies[currency][2]
                right_base = True

            if currencies[currency][0] in quote:
                quote = currency
                quote_unit = currencies[currency][2]
                right_quote = True

        if not right_base:
            raise APIException(f'Ошиблись в написании валюты «{base}»')

        if not right_quote:
            raise APIException(f'Ошиблись в написании валюты «{quote}»')

        r = requests.get(
            f'https://min-api.cryptocompare.com/data/price?fsym={base}'
            f'&tsyms={quote}')
        total_base = json.loads(r.content)[quote]

        return total_base, base_unit, quote_unit

    @staticmethod
    def pretty_number(number, number_type: str):
        if number_type == 'float':
            number = round(float(number), 2)
            number = '{0:,}'.format(number).replace(',', ' ')
            number = number.split('.')
            number = ','.join(number)

        if number_type == 'int':
            number = int(number)
            number = '{0:,}'.format(number).replace(',', ' ')

        return number
