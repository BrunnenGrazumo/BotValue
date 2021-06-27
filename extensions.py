import json
import requests
from config import exchanger


class ConverterException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(values):

        if len(values) != 3:
            raise ValueError("Неверный формат ввода\n/help")
        quote, base, amount = values

        if quote == base:
            raise ConverterException("Нет смысла вводить одинаковые валюты")

        try:
            quote_formated = exchanger[quote]
        except KeyError:
            raise ConverterException(f'Валюты {quote} нет в списке доступных: /values')

        try:
            base_formated = exchanger[base]
        except KeyError:
            raise ConverterException(f'Валюты {base} нет в списке доступных:\n/values')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f'Введите корректное количество валюты. \n{amount} - некорректное')

        if amount <= 0:
            raise ConverterException(f'Введите корректное количество валюты. \n{amount} - некорректное')

        r = requests.get(f'https://free.currconv.com/api/v7/convert?q={quote_formated}_{base_formated}&compact=ultra&\
apiKey=685eafcd6ea4cdd61f6a')
        result = float(json.loads(r.content)[f'{quote_formated}_{base_formated}'])*float(amount)
        return round(result, 2), quote_formated, base_formated



