import json
import requests


def create_currencies_dict(table):
    url = 'https://api.nbp.pl/api/exchangerates/tables/' + table + '/?format=json'
    r = requests.get(url)
    response = json.loads(r.text)
    dict_string = '{'
    for i in response[0]['rates']:
        dict_string += "'" + i['currency'] + "'" + ': ' + "'" + i['code'] + "'" + ', '
    dict_string = dict_string[:-2] + '}'

    return dict_string


if __name__ == '__main__':
    print(create_currencies_dict('a'))

