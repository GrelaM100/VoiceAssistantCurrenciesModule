import requests
import json
from googletrans import Translator
from text_to_num import alpha2digit

NBP_API = "http://api.nbp.pl/api/exchangerates/rates/"
A_TABLE_CURRENCIES = {'bat': 'THB', 'dolar amerykański': 'USD', 'dolar australijski': 'AUD', 'dolar Hongkongu': 'HKD',
                      'dolar kanadyjski': 'CAD', 'dolar nowozelandzki': 'NZD', 'dolar singapurski': 'SGD', 'euro': 'EUR',
                      'forint': 'HUF', 'frank szwajcarski': 'CHF', 'funt szterling': 'GBP', 'hrywna': 'UAH',
                      'jen': 'JPY', 'korona czeska': 'CZK', 'korona duńska': 'DKK', 'korona islandzka': 'ISK',
                      'korona norweska': 'NOK', 'korona szwedzka': 'SEK', 'kuna': 'HRK', 'lej rumuński': 'RON',
                      'lew': 'BGN', 'lira turecka': 'TRY', 'nowy izraelski szekel': 'ILS', 'peso chilijskie': 'CLP',
                      'peso filipińskie': 'PHP', 'peso meksykańskie': 'MXN', 'rand': 'ZAR', 'real': 'BRL',
                      'ringgit': 'MYR', 'rubel rosyjski': 'RUB', 'rupia indonezyjska': 'IDR', 'rupia indyjska': 'INR',
                      'won południowokoreański': 'KRW', 'yuan renminbi': 'CNY', 'SDR': 'XDR'}

B_TABLE_CURRENCIES = {'afgani': 'AFN', 'ariary': 'MGA', 'balboa': 'PAB',
                      'birr etiopski': 'ETB', 'boliwar soberano': 'VES', 'boliwiano': 'BOB', 'colon kostarykański': 'CRC',
                      'colon salwadorski': 'SVC', 'cordoba oro': 'NIO', 'dalasi': 'GMD', 'denar': 'MKD',
                      'dinar algierski': 'DZD', 'dinar bahrajski': 'BHD', 'dinar iracki': 'IQD', 'dinar jordański': 'JOD',
                      'dinar kuwejcki': 'KWD', 'dinar libijski': 'LYD', 'dinar serbski': 'RSD', 'dinar tunezyjski': 'TND',
                      'dirham marokański': 'MAD', 'dirham': 'AED', 'dobra': 'STN', 'dolar bahamski': 'BSD',
                      'dolar barbadoski': 'BBD', 'dolar belizeński': 'BZD', 'dolar brunejski': 'BND',
                      'dolar Fidżi': 'FJD', 'dolar gujański': 'GYD', 'dolar jamajski': 'JMD', 'dolar liberyjski':
                          'LRD', 'dolar namibijski': 'NAD', 'dolar surinamski': 'SRD', 'dolar Trynidadu i Tobago': 'TTD',
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

MONTHS_TO_NUM = {'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6, 'lipca': 7,
                 'sierpnia': 8, 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12}


def get_api_response(table, currency, from_date='/', to_date=''):
    if from_date != '/':
        from_date = '/' + from_date + '/'
    if to_date != '/':
        to_date = '/' + to_date + '/'

    url = NBP_API + table + '/' + currency + from_date + to_date + '?format=json'
    request = requests.get(url)
    response = json.loads(request.text)
    return response


def get_mid_exchange_rate_single_currency(currency):
    if currency in A_TABLE_CURRENCIES:
        table = 'a'
        currency_code = A_TABLE_CURRENCIES[currency].lower()
    elif currency in B_TABLE_CURRENCIES:
        table = 'b'
        currency_code = B_TABLE_CURRENCIES[currency].lower()
    else:
        return

    currency_data = get_api_response(table, currency_code)
    value = currency_data['rates'][0]['mid']
    return value


def get_current_mid_exchange_rate(currencies):
    values = []
    for curr in currencies:
        if curr == 'złoty':
            values.append(1)
        else:
            values.append(get_mid_exchange_rate_single_currency(curr))

    value = values[0] / values[1]
    return "Aktualny średni kurs " + currencies[0] + " do " + currencies[1] + " wynosi około " + str(round(value, 2))


def text_day_to_num(day):
    translator = Translator()
    translation = translator.translate(day, dest='en')
    translation = translation.text.lower()
    if translation == 'first':
        return 1
    elif translation == 'second':
        return 2
    elif translation == 'third':
        return 3
    else:
        num = alpha2digit(translation, 'en').replace('the ', '').replace('st', '').replace('nd', '').replace('rd', '').\
            replace('th', '')

        return num


def text_year_to_num(year):
    translator = Translator()
    translation = translator.translate(year, dest='en')
    num = alpha2digit(translation.text.lower(), 'en').replace('st', '').replace('nd', '').replace('rd', '').\
        replace('th', '').replace('s', '')
    if ' a ' in num:
        num = int(num.split(' a ')[0]) + int(num.split(' a ')[1].split()[0])
        num = str(num)

    num = num.split()[0]
    if int(num) < 2002 or int(num) > 2022:
        raise ValueError
    return num


def prepare_date(date_text):
    month = ''
    for element in date_text.split():
        if element in MONTHS_TO_NUM:
            month = element
            break
    day_year_split = date_text.split(' ' + month + ' ')
    day = text_day_to_num(day_year_split[0])
    month = MONTHS_TO_NUM[month]
    year = text_year_to_num(day_year_split[1])
    date = year + '-'
    date += str(month) + '-'
    date += day

    return date


def get_mid_exchange_rate_by_date(currencies, date_text):
    pass


if __name__ == '__main__':
    while True:
        query = input()
        test = query.split(' kurs ')
        if len(test) == 2:
            currencies = test[1].split(' do ')
            check = test[0]
            if check in ['Jaki jest teraźniejszy', 'Jaki jest', 'Jaki jest obecny', 'Jaki jest bieżący',
                         'Jaki jest średni', 'Jaki jest teraźniejszy średni', 'Jaki jest obecny średni',
                         'Jaki jest bieżący średni']:
                print(get_current_mid_exchange_rate(currencies))

            if check in ['Jaki był', 'Ile wynosił', 'Jaką miał wartość', 'Jaki był średni', 'Ile wynosił średni',
                         'Jaką miał wartość średni']:
                curr_date = currencies[1].split(' dnia ')
                currencies[1] = curr_date[0]
                date_text = curr_date[1]

                print(currencies)
                print(prepare_date(date_text))


