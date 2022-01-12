import requests
import json
from datetime import date

NBP_API = "http://api.nbp.pl/api/exchangerates/rates/"
A_TABLE_CURRENCIES = {'bat': 'THB', 'dolar amerykański': 'USD', 'dolar australijski': 'AUD', 'dolar Hongkongu': 'HKD',
                      'dolar kanadyjski': 'CAD', 'dolar nowozelandzki': 'NZD', 'dolar singapurski': 'SGD',
                      'euro': 'EUR',
                      'forint': 'HUF', 'frank szwajcarski': 'CHF', 'funt szterling': 'GBP', 'hrywna': 'UAH',
                      'jen': 'JPY', 'korona czeska': 'CZK', 'korona duńska': 'DKK', 'korona islandzka': 'ISK',
                      'korona norweska': 'NOK', 'korona szwedzka': 'SEK', 'kuna': 'HRK', 'lej rumuński': 'RON',
                      'lew': 'BGN', 'lira turecka': 'TRY', 'nowy izraelski szekel': 'ILS', 'peso chilijskie': 'CLP',
                      'peso filipińskie': 'PHP', 'peso meksykańskie': 'MXN', 'rand': 'ZAR', 'real': 'BRL',
                      'ringgit': 'MYR', 'rubel rosyjski': 'RUB', 'rupia indonezyjska': 'IDR', 'rupia indyjska': 'INR',
                      'won południowokoreański': 'KRW', 'yuan renminbi': 'CNY', 'SDR': 'XDR'}

B_TABLE_CURRENCIES = {'afgani': 'AFN', 'ariary': 'MGA', 'balboa': 'PAB',
                      'birr etiopski': 'ETB', 'boliwar soberano': 'VES', 'boliwiano': 'BOB',
                      'colon kostarykański': 'CRC',
                      'colon salwadorski': 'SVC', 'cordoba oro': 'NIO', 'dalasi': 'GMD', 'denar': 'MKD',
                      'dinar algierski': 'DZD', 'dinar bahrajski': 'BHD', 'dinar iracki': 'IQD',
                      'dinar jordański': 'JOD',
                      'dinar kuwejcki': 'KWD', 'dinar libijski': 'LYD', 'dinar serbski': 'RSD',
                      'dinar tunezyjski': 'TND',
                      'dirham marokański': 'MAD', 'dirham': 'AED', 'dobra': 'STN', 'dolar bahamski': 'BSD',
                      'dolar barbadoski': 'BBD', 'dolar belizeński': 'BZD', 'dolar brunejski': 'BND',
                      'dolar Fidżi': 'FJD', 'dolar gujański': 'GYD', 'dolar jamajski': 'JMD', 'dolar liberyjski':
                          'LRD', 'dolar namibijski': 'NAD', 'dolar surinamski': 'SRD',
                      'dolar Trynidadu i Tobago': 'TTD',
                      'dolar wschodniokaraibski': 'XCD', 'dolar Wysp Salomona': 'SBD', 'dolar Zimbabwe': 'ZWL',
                      'dong': 'VND', 'dram': 'AMD', 'escudo Zielonego Przylądka': 'CVE', 'florin arubański': 'AWG',
                      'frank burundyjski': 'BIF', 'frank CFA BCEAO ': 'XOF', 'frank CFA BEAC': 'XAF',
                      'frank CFP  ': 'XPF', 'frank Dżibuti': 'DJF', 'frank gwinejski': 'GNF', 'frank Komorów': 'KMF',
                      'frank kongijski': 'CDF', 'frank rwandyjski': 'RWF', 'funt egipski': 'EGP',
                      'funt gibraltarski': 'GIP', 'funt libański': 'LBP', 'funt południowosudański': 'SSP',
                      'funt sudański': 'SDG', 'funt syryjski': 'SYP', 'Ghana cedi ': 'GHS', 'gourde': 'HTG',
                      'guarani': 'PYG', 'gulden Antyli Holenderskich': 'ANG', 'kina': 'PGK', 'kip': 'LAK',
                      'kwacha malawijska': 'MWK', 'kwacha zambijska': 'ZMW', 'kwanza': 'AOA', 'kyat': 'MMK',
                      'lari': 'GEL', 'lej Mołdawii': 'MDL', 'lek': 'ALL', 'lempira': 'HNL', 'leone': 'SLL',
                      'lilangeni': 'SZL', 'loti': 'LSL', 'manat azerbejdżański': 'AZN', 'metical': 'MZN',
                      'naira': 'NGN', 'nakfa': 'ERN', 'nowy dolar tajwański': 'TWD', 'nowy manat': 'TMT',
                      'ouguiya': 'MRU', 'pa anga': 'TOP', 'pataca': 'MOP', 'peso argentyńskie': 'ARS',
                      'peso dominikańskie': 'DOP', 'peso kolumbijskie': 'COP', 'peso kubańskie': 'CUP',
                      'peso urugwajskie': 'UYU', 'pula': 'BWP', 'quetzal': 'GTQ', 'rial irański': 'IRR',
                      'rial jemeński': 'YER', 'rial katarski': 'QAR', 'rial omański': 'OMR', 'rial saudyjski': 'SAR',
                      'riel': 'KHR', 'rubel białoruski': 'BYN', 'rupia lankijska': 'LKR', 'rupia': 'MVR',
                      'rupia Mauritiusu': 'MUR', 'rupia nepalska': 'NPR', 'rupia pakistańska': 'PKR',
                      'rupia seszelska': 'SCR', 'sol': 'PEN', 'som': 'KGS', 'somoni': 'TJS', 'sum': 'UZS',
                      'szyling kenijski': 'KES', 'szyling somalijski': 'SOS', 'szyling tanzański': 'TZS',
                      'szyling ugandyjski': 'UGX', 'taka': 'BDT', 'tala': 'WST', 'tenge': 'KZT', 'tugrik': 'MNT',
                      'vatu': 'VUV', 'wymienialna marka': 'BAM'}

MONTHS_TO_NUM = {'stycznia': '01', 'lutego': '02', 'marca': '03', 'kwietnia': '04', 'maja': '05', 'czerwca': '06',
                 'lipca': '07', 'sierpnia': '08', 'września': '09', 'października': '10', 'listopada': '11',
                 'grudnia': '12'}


def get_api_response(table, currency, from_date='/', to_date=''):
    if from_date != '/':
        from_date = '/' + from_date + '/'
    if to_date != '':
        to_date = '/' + to_date + '/'

    url = NBP_API + table + '/' + currency + from_date + to_date + '?format=json'
    request = requests.get(url)
    if request.status_code == 404:
        raise ValueError #TODO
    response = json.loads(request.text)
    return response


def get_exchange_rate_single_currency(currency, from_date='/', to_date='', rate='mid'):
    if currency in A_TABLE_CURRENCIES:
        table = 'a'
        currency_code = A_TABLE_CURRENCIES[currency].lower()
    elif currency in B_TABLE_CURRENCIES:
        table = 'b'
        currency_code = B_TABLE_CURRENCIES[currency].lower()
    else:
        return

    if rate != 'mid':
        table = 'c'

    currency_data = get_api_response(table, currency_code, from_date, to_date)
    value = currency_data['rates'][0][rate]
    return value


def get_current_exchange_rate(currencies):
    values = []
    for curr in currencies:
        if curr == 'złoty':
            values.append(1)
        else:
            values.append(get_exchange_rate_single_currency(curr))

    value = values[0] / values[1]
    return value


def get_current_exchange_rate_response(currencies):
    value = str(round(get_current_exchange_rate(currencies)))
    return "Aktualny średni kurs " + currencies[0] + " do " + currencies[1] + " wynosi około " + value


def get_date_from_text(text):
    day = ''
    month = ''
    year = ''
    for element in text.split():
        if element.isdigit():
            if day == '':
                day = element
            else:
                year = element
        if element in MONTHS_TO_NUM:
            month = MONTHS_TO_NUM[element]

    if day != '' and month != '' and year != '':
        if int(day) not in range(1, 32):
            raise ValueError #TODO
        if int(year) not in range(2002, 2023):
            raise ValueError

        concat_date = year + '-' + month + '-' + day
        return concat_date

    raise AttributeError


def get_exchange_rate_by_date(currencies, given_date):
    values = []
    for curr in currencies:
        if curr == 'złoty':
            values.append(1)
        else:
            values.append(get_exchange_rate_single_currency(curr, given_date))

    value = values[0] / values[1]
    return value


def get_exchange_rate_by_date_response(currencies, given_date):
    given_date = get_date_from_text(given_date)
    value = str(round(get_exchange_rate_by_date(currencies, given_date), 2))
    return "Dnia " + given_date + " średni kurs " + currencies[0] + " do " + currencies[1] + " wynosił około " + value


def get_currencies_from_text(text):
    text = text.split(' do ')
    if len(text) == 1:
        return None #TODO
    first_currency = text[0]
    second_currency = ''
    for element in text[1].split():
        second_currency += element
        if second_currency in A_TABLE_CURRENCIES or second_currency in B_TABLE_CURRENCIES or second_currency == 'złoty':
            break
        second_currency += ' '

    if second_currency not in A_TABLE_CURRENCIES and second_currency not in B_TABLE_CURRENCIES \
            and second_currency != 'złoty':
        return None

    return [first_currency, second_currency]


def check_difference_between_dates(text, currencies):
    text = text.split(' od ')[1]
    dates = text.split(' do ')
    values = []
    for given_date in dates:
        given_date = get_date_from_text(given_date)
        values.append(get_exchange_rate_by_date(currencies, given_date))
    if len(dates) == 1:
        second_date = date.today().strftime("%Y-%m-%d")
        values.append(get_exchange_rate_by_date(currencies, second_date))

    return values[1] - values[0]


def get_difference_between_dates_response(text, currencies):
    difference = check_difference_between_dates(text, currencies)
    if difference < 0:
        return 'Średni kurs ' + currencies[0] + ' do ' + currencies[1] + ' zmalał o około ' + \
               str(round(difference, 2))[1:]
    elif difference > 0:
        return 'Średni kurs ' + currencies[0] + ' do ' + currencies[1] + ' wzrósł o około ' + str(round(difference, 2))
    else:
        return 'Średni kurs ' + currencies[0] + ' do ' + currencies[1] + ' nie zmienił się'


if __name__ == '__main__':
    while True:
        query = input()
        test = query.split(' kurs ')
        if len(test) == 2:
            currencies = get_currencies_from_text(test[1])  # TODO if None then currency not found
            check = test[0]
            if check in ['Jaki jest teraźniejszy', 'Jaki jest', 'Jaki jest obecny', 'Jaki jest bieżący',
                         'Jaki jest średni', 'Jaki jest teraźniejszy średni', 'Jaki jest obecny średni',
                         'Jaki jest bieżący średni']:
                print(get_current_exchange_rate_response(currencies))

            if check in ['Jaki był', 'Ile wynosił', 'Jaką miał wartość', 'Jaki był średni', 'Ile wynosił średni',
                         'Jaką miał wartość średni']:
                print(get_exchange_rate_by_date_response(currencies, test[1]))

            if check in ['Jak zmienił się']:
                print(get_difference_between_dates_response(test[1], currencies))
