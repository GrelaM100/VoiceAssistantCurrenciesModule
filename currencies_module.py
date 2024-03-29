import requests
import json
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import calendar
import exceptions as exc

NBP_API = "http://api.nbp.pl/api/exchangerates/rates/"
# słownik walut z tabeli A na kod tych walut, do tworzenia zapytań wykorzystuje się kody walut, słowniki poniżej służą
# konwersji nazwy waluty na jej kod
A_TABLE_CURRENCIES = {'bata': 'THB', 'dolara amerykańskiego': 'USD', 'dolara australijskiego': 'AUD',
                      'dolara hongkońskiego': 'HKD', 'dolara kanadyjskiego': 'CAD', 'dolara nowozelandzkiego': 'NZD',
                      'dolara singapurskiego': 'SGD', 'euro': 'EUR', 'forinta': 'HUF', 'franka szwajcarskiego': 'CHF',
                      'funta szterlinga': 'GBP', 'hrywny': 'UAH', 'jena': 'JPY', 'korony czeskiej': 'CZK',
                      'korony duńskiej': 'DKK', 'korony islandzkiej': 'ISK', 'korony norweskiej': 'NOK',
                      'korony szwedzkiej': 'SEK', 'kuny': 'HRK', 'leja rumuńskiego': 'RON', 'lewa': 'BGN',
                      'liry tureckiej': 'TRY', 'szekla izraelskiego': 'ILS', 'peso chilijskiego': 'CLP',
                      'peso filipińskiego': 'PHP', 'peso meksykańskiego': 'MXN', 'randa': 'ZAR', 'reala': 'BRL',
                      'ringgita': 'MYR', 'rubla rosyjskiego': 'RUB', 'rupii indonezyjskiej': 'IDR',
                      'rupii indyjskiej': 'INR', 'wona południowokoreańskiego': 'KRW', 'juana': 'CNY',
                      'renminbi': 'CNY'}

# wybrane, specjalne waluty z tabeli A. Przykładowo kiedy użytkownik pyta o walutę dolar zakłada się, że chodzi mu o
# dolar amerykański, dzięki temu zapytania są bardziej intuicyjne
SPECIAL_A_TABLE_CURRENCIES = {'dolara': 'USD', 'franka': 'CHF', 'funta': 'GBP', 'leja': 'RON', 'liry': 'TRY',
                              'szekla': 'ILS', 'peso': 'MXN', 'rubla': 'RUB', 'rupii': 'INR', 'wona': 'KRW'}

# waluty z tabeli B
B_TABLE_CURRENCIES = {'afgani': 'AFN', 'ariary': 'MGA', 'balboa': 'PAB', 'birra': 'ETB', 'boliwara': 'VES',
                      'boliwiano': 'BOB', 'kolona kostarykańskiego': 'CRC', 'kolona salwadorskiego': 'SVC',
                      'kordoby': 'NIO', 'dalasi': 'GMD', 'denara': 'MKD', 'dinara algierskiego': 'DZD',
                      'dinara bahrajskiego': 'BHD', 'dinara irackiego': 'IQD', 'dinara jordańskiego': 'JOD',
                      'dinara kuwejckiego': 'KWD', 'dinara libijskiego': 'LYD', 'dinara serbskiego': 'RSD',
                      'dinar tunezyjskiego': 'TND', 'dirhama marokańskiego': 'MAD', 'dirhama': 'AED', 'dobry': 'STN',
                      'dolara bahamskiego': 'BSD', 'dolara barbadoskiego': 'BBD', 'dolara belizeńskiego': 'BZD',
                      'dolara brunejskiego': 'BND', 'dolara fidżi': 'FJD', 'dolara gujańskiegp': 'GYD',
                      'dolara jamajskiego': 'JMD', 'dolara liberyjskiego': 'LRD', 'dolara namibijskiego': 'NAD',
                      'dolara surinamskiego': 'SRD', 'dolara trynidadu i tobago': 'TTD',
                      'dolara wschodniokaraibskiego': 'XCD', 'dolara wysp salomona': 'SBD', 'dolara zimbabwe': 'ZWL',
                      'donga': 'VND', 'drama': 'AMD', 'eskudo': 'CVE', 'florina arubańskiego': 'AWG',
                      'franka burundyjskiego': 'BIF', 'franka dżibuti': 'DJF', 'franka gwinejskiego': 'GNF',
                      'franka komorów': 'KMF', 'franka kongijskiego': 'CDF', 'franka rwandyjskiego': 'RWF',
                      'funta egipskiego': 'EGP', 'funta gibraltarski': 'GIP', 'funta libańskiego': 'LBP',
                      'funta południowosudańskiego': 'SSP', 'funta sudańskiego': 'SDG', 'funta syryjskiego': 'SYP',
                      'gurda': 'HTG', 'guarani': 'PYG', 'kina': 'PGK', 'kipa': 'LAK',
                      'kwacha malawijskiego': 'MWK', 'kwacha zambijskiego': 'ZMW', 'kwanzy': 'AOA', 'kiata': 'MMK',
                      'lari': 'GEL', 'leja mołdawii': 'MDL', 'leka': 'ALL', 'lempiry': 'HNL', 'leone': 'SLL',
                      'lilangeni': 'SZL', 'loti': 'LSL', 'manata azerbejdżańskiego': 'AZN', 'metikala': 'MZN',
                      'nairy': 'NGN', 'nakfy': 'ERN', 'nowego dolara tajwańskiego': 'TWD', 'nowego manata': 'TMT',
                      'ouguiya': 'MRU', 'pa angi': 'TOP', 'pataka': 'MOP', 'peso argentyńskiego': 'ARS',
                      'peso dominikańskiego': 'DOP', 'peso kolumbijskiego': 'COP', 'peso kubańskiego': 'CUP',
                      'peso urugwajskiego': 'UYU', 'puli': 'BWP', 'quetzala': 'GTQ', 'riala irańskiego': 'IRR',
                      'riala jemeńskiego': 'YER', 'riala katarskiego': 'QAR', 'riala omańskiego': 'OMR',
                      'riala saudyjskiego': 'SAR', 'riela': 'KHR', 'rubla białoruskiego': 'BYN',
                      'rupii lankijskiej': 'LKR', 'rupii mauritiusu': 'MUR', 'rupii nepalskiej': 'NPR',
                      'rupii pakistańskiej': 'PKR', 'rupii seszelskiej': 'SCR', 'sola': 'PEN', 'somy': 'KGS',
                      'somoni': 'TJS', 'sum': 'UZS', 'szylinga kenijskiego': 'KES', 'szylinga somalijskiego': 'SOS',
                      'szylinga tanzańskiego': 'TZS', 'szylinga ugandyjskiego': 'UGX', 'taki': 'BDT', 'tala': 'WST',
                      'tenge': 'KZT', 'tugrika': 'MNT', 'watu': 'VUV'}

# słownik służący konwersji nazw miesięcy na liczby do zapytań
MONTHS_TO_NUM = {'stycznia': '01', 'lutego': '02', 'marca': '03', 'kwietnia': '04', 'maja': '05', 'czerwca': '06',
                 'lipca': '07', 'sierpnia': '08', 'września': '09', 'października': '10', 'listopada': '11',
                 'grudnia': '12'}


def get_api_response(table, currency, from_date='/', to_date=''):
    """ Funkcja zwraca dane zwrócone z API NBP w postaci JSON

        Jeżeli argumenty 'from_date' oraz 'to_date' nie zostaną podane, wykorzystując ich wartości domyślne,
        pobrany zostanie obecnie obowiazujący kurs waluty.

        Argumenty
        ---------
        table : str
            Tabela, w której znajduje się dana waluta
        currency : str
            Kod waluty
        from_date : str, opcjonalny
            Data w postaci ciągu znaków od której mają zostać pobrane dane, domyślna wartość to '/'
        to_date : str, opcjonalny
            Data w postaci ciągu znaków do której mają zostać pobrane dane, domyślna wartość to pusty ciąg znaków

        Wyjątki
        -------
        NotFoundException
            Wyrzucany jeżeli podane dane nie zostaną odnalezione i API zwróci kod 404. Przykładowo może się tak stać
            kiedy podana data jest z przyszłości.
    """

    if from_date != '/':
        from_date = '/' + from_date + '/'
    if to_date != '':
        to_date = '/' + to_date + '/'

    url = NBP_API + table + '/' + currency + from_date + to_date + '?format=json'
    request = requests.get(url)
    if request.status_code == 404:
        raise exc.NotFoundException
    response = json.loads(request.text)
    return response


def find_table_and_rate(currency, rate):
    """ Funkcja zwraca tabelę oraz kod podanej waluty

        Argumenty
        ---------
        currency : str
            Nazwa waluty
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży

            Służy przypisaniu tabeli C w przypadku, gdy użytkownik pyta o kurs kupna lub sprzedaży

        Wyjątki
        -------
        InvalidCurrency
            Wyrzucany jeżeli podana waluta nie została znaleziona w tabali A i B
    """
    if currency in SPECIAL_A_TABLE_CURRENCIES:
        table = 'a'
        currency_code = SPECIAL_A_TABLE_CURRENCIES[currency].lower()
    elif currency in A_TABLE_CURRENCIES:
        table = 'a'
        currency_code = A_TABLE_CURRENCIES[currency].lower()
    elif currency in B_TABLE_CURRENCIES:
        table = 'b'
        currency_code = B_TABLE_CURRENCIES[currency].lower()
    else:
        raise exc.InvalidCurrency

    if rate == 'bid' or rate == 'ask':
        table = 'c'

    return table, currency_code


def get_exchange_rate_single_currency(currency, rate, from_date='/', to_date=''):
    """ Funkcja zwraca wartość kursu podanej waluty do złotego

        Argumenty
        ---------
        currency : str
            Nazwa walty
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
        from_date : str, opcjonalny
            Data w postaci ciągu znaków od której mają zostać pobrane dane, domyślna wartość to '/'
        to_date : str, opcjonalny
            Data w postaci ciągu znaków do której mają zostać pobrane dane, domyślna wartość to pusty ciąg znaków
    """
    table, currency_code = find_table_and_rate(currency, rate)
    currency_data = get_api_response(table, currency_code, from_date, to_date)
    value = currency_data['rates'][0][rate]
    return value


def get_current_exchange_rate(currencies, rate):
    """ Funkcja do obliczania kursu dwóch podanych walut na podstawie ich kursu do złotego

        Argumenty
        ---------
        currencies : list
            Lista zawierająca dwie nazwy walut
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
    """
    values = []
    for curr in currencies:
        if curr == 'złotego':
            values.append(1)
        else:
            values.append(get_exchange_rate_single_currency(curr, rate))

    value = values[0] / values[1]
    return value


def get_current_exchange_rate_response(currencies, rate):
    """ Funkcja do zwrócenia odpowiedniej informacji o aktualnym kursie podanych walut

        Argumenty
        ---------
        currencies : list
            Lista zawierająca dwie nazwy walut
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
    """
    value = str(round(get_current_exchange_rate(currencies, rate), 2)).replace('.', ',')
    rate_text = rate_to_text(rate)
    return 'Aktualny' + rate_text + currencies[0] + ' do ' + currencies[1] + ' wynosi około ' + value


def validate_date(date_to_validate):
    """ Funkcja do walidacji podanej daty

        Argumenty
        ---------
        date_to_validate : str
            Data do walidacji podana w postaci ciągu znaków

        Wyjątki
        -------
        NotFoundException
            Wyrzucany ww przypadku podania przyszłej daty lub daty przed 2 stycznia 2002 roku, ponieważ od tej daty
            przechowywane są dane archiwalne dla kursów walut

        InvalidDateException
            Wyrzucany w przypadku podania nieprawidłowego ciągu znaków, którego nie można skonwertować na datę
    """
    try:
        date_object = datetime.strptime(date_to_validate, '%Y-%m-%d')
        if date_object > datetime.today() or date_object < datetime(2002, 1, 2):
            raise exc.NotFoundException
    except ValueError:
        raise exc.InvalidDateException


def get_date_from_text(text):
    """ Funkcja zwracają datę z podanego tekstu w postaci ciągu znaków

        Argumenty
        ---------
        text : str
            Tekst zawierający datę

        Wyjątki
        -------
        MissingDate
            Wyrzucany w przypadku, gdy w podanym tekście nie podano pełnej daty, to znaczy nie podano dnia miesiąca lub
            roku
    """
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
        if len(day) == 1:
            day = '0' + day
        concat_date = year + '-' + month + '-' + day
        validate_date(concat_date)

        return concat_date

    raise exc.MissingDate


def rate_to_text(rate):
    """ Funkcja zwracająca typ kursu w postaci ciągu znaków

        Argumenty
        ---------
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
    """
    if rate == 'ask':
        rate_text = ' kurs sprzedaży '
    elif rate == 'bid':
        rate_text = ' kurs kupna '
    else:
        rate_text = ' średni kurs '

    return rate_text


def get_exchange_rate_by_date(currencies, given_date, rate):
    """ Funkcja do obliczania kursu dwóch podanych walut na podstawie ich kursu do złotego w podanym dniu

            Argumenty
            ---------
            currencies : list
                Lista zawierająca dwie nazwy walut
            given_date : str
                Podana data w postaci ciągu znaków
            rate : str
                Jedna z wartości:
                'mid' - średni kurs
                'bid' - kurs kupna
                'ask' - kurs sprzedaży
        """
    values = []
    for curr in currencies:
        if curr == 'złotego':
            values.append(1)
        else:
            values.append(get_exchange_rate_single_currency(curr, rate, given_date))

    value = values[0] / values[1]
    return value


def get_exchange_rate_by_date_response(currencies, given_date, rate):
    """ Funkcja do zwrócenia odpowiedniej informacji o kursie podanych walut, w podanym dniu

            Argumenty
            ---------
            currencies : list
                Lista zawierająca dwie nazwy walut
            given_date : str
                Podana data w postaci ciągu znaków
            rate : str
                Jedna z wartości:
                'mid' - średni kurs
                'bid' - kurs kupna
                'ask' - kurs sprzedaży
        """
    given_date = get_date_from_text(given_date)
    value = str(round(get_exchange_rate_by_date(currencies, given_date, rate), 2)).replace('.', ',')
    rate_text = rate_to_text(rate)
    return 'Dnia ' + given_date + rate_text + currencies[0] + ' do ' + currencies[1] + ' wynosił około ' + value


def get_currencies_from_text(text):
    """ Funkcja zwraca listę dwóch walut na podstawie tekstu

        Argumenty
        ---------
        text : str
            Tekst zawierajacy nazwy walut

        Wyjątki
        -------
        OnlyOneCurrency
            Wyrzucany w przypadku podania w tekście tylko jednej nazwy waluty
        InvalidCurrency
            Wyrzucany, gdy nie znaleziono waluty o podanej nazwie
    """
    text = text.split(' do ')
    if len(text) == 1:
        raise exc.OnlyOneCurrency
    first_currency = text[0]
    second_currency = ''
    for element in text[1].split():
        second_currency += element
        if second_currency in A_TABLE_CURRENCIES or second_currency in B_TABLE_CURRENCIES or \
                second_currency == 'złotego':
            break
        second_currency += ' '

    if second_currency not in A_TABLE_CURRENCIES and second_currency not in B_TABLE_CURRENCIES:
        second_currency = ''
        for element in text[1].split():
            second_currency += element
            if second_currency in SPECIAL_A_TABLE_CURRENCIES or second_currency == 'złotego':
                break
            second_currency += ' '

    if second_currency not in SPECIAL_A_TABLE_CURRENCIES and second_currency not in A_TABLE_CURRENCIES and \
            second_currency not in B_TABLE_CURRENCIES and second_currency != 'złotego':
        raise exc.InvalidCurrency

    return [first_currency, second_currency]


def check_difference_between_dates(text, currencies, rate):
    """ Funkcja do obliczania różnicy kursu podanych walut między podanymi datami

        Argumenty
        ---------
        text : str
            Tekst zawierajacy nazwy walut oraz daty
        currencies : list
                Lista zawierająca dwie nazwy walut
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
    """
    text = text.split(' od ')[1]
    dates = text.split(' do ')
    values = []
    for given_date in dates:
        given_date = get_date_from_text(given_date)
        values.append(get_exchange_rate_by_date(currencies, given_date, rate))
    if len(dates) == 1:
        second_date = date.today().strftime('%Y-%m-%d')
        values.append(get_exchange_rate_by_date(currencies, second_date, rate))

    return values[1] - values[0]


def get_difference_between_dates_response(text, currencies, rate):
    """ Funkcja do zwracania infromacji o różnicy kursu podanych walut między podanymi datami

        Argumenty
        ---------
        text : str
            Tekst zawierajacy nazwy walut oraz daty
        currencies : list
                Lista zawierająca dwie nazwy walut
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
        """
    difference = check_difference_between_dates(text, currencies, rate)
    rate_text = rate_to_text(rate)
    rate_text = rate_text.lstrip().rstrip()
    rate_text = rate_text.capitalize() + ' '
    difference = round(difference, 2)
    if difference < 0:
        return rate_text + currencies[0] + ' do ' + currencies[1] + ' zmalał o około ' + \
               str(round(difference, 2))[1:].replace('.', ',')
    elif difference > 0:
        return rate_text + currencies[0] + ' do ' + currencies[1] + ' wzrósł o około ' + \
               str(difference).replace('.', ',')
    else:
        return rate_text + currencies[0] + ' do ' + currencies[1] + ' nie zmienił się'


def check_code_in_table(table, word):
    """ Funkcja zwraca kod oraz nazwę waluty na podstawie podanej tabeli oraz słowa

        Argumenty
        ---------
        table : dict
            Słownik reprezentujący tabelę walut
        word : str
            Dowolne słowo, które potencjalnie jest kodem waluty
    """
    code = ''
    curr = ''
    for code_in_table in table.values():
        if word == code_in_table:
            code = code_in_table
            curr = list(table.keys())[list(table.values()).index(code)]
            break

    return code, curr


def check_currency_in_table(table, query):
    """ Funkcja zwraca kod oraz nazwę waluty na podstawie podanej tabeli oraz zapytania

        Argumenty
        ---------
        table : dict
            Słownik reprezentujący tabelę walut
        word : str
            Dowolne zapytanie, w którym potencjalnie znajduje się nazwa waluty
    """
    code = ''
    curr = ''

    for currency in table.keys():
        if currency in query:
            code = table[currency]
            curr = currency
            break

    return code, curr


def get_currency_by_code(query):
    """ Funkcja zwracająca infromację o tym która waluta posiada kod z zapytania

        Argumenty
        ---------
        query : str
            Dowolne zapytanie

        Wyjątki
        -------
        CodeNotFound
            Wyrzucany w przypadku nie znalezienia waluty o podanym kodzie
    """
    words = query.split()
    code = ''
    curr = ''
    for word in words:
        word = word.upper()
        code, curr = check_code_in_table(SPECIAL_A_TABLE_CURRENCIES, word)

        if code == '' and curr == '':
            code, curr = check_code_in_table(A_TABLE_CURRENCIES, word)

        if code == '' and curr == '':
            code, curr = check_code_in_table(B_TABLE_CURRENCIES, word)

    if code == '':
        raise exc.CodeNotFound

    return 'Kod ' + code + ' to kod ' + curr


def get_code_by_currency(query):
    """ Funkcja zwracająca informację o kodzie podanej w zapytaniu waluty

        Argumenty
        ---------
        query : str
            Dowolne zapytanie

        Wyjątki
        -------
        InvalidCurrency
            Wyrzucany w przypadku nie odnalezienia waluty o podanej nazwie
    """
    code, curr = check_currency_in_table(A_TABLE_CURRENCIES, query)
    if code == '' and curr == '':
        code, curr = check_currency_in_table(B_TABLE_CURRENCIES, query)
    if code == '' and curr == '':
        code, curr = check_currency_in_table(SPECIAL_A_TABLE_CURRENCIES, query)
    if code == '' and curr == '':
        raise exc.InvalidCurrency

    return 'Kod ' + curr + ' to ' + code


def get_currencies_to_compare(text):
    """ Funkcja zwracająca listę nazw dwóch walut do porównania ich kursów

        Argumenty
        ---------
        text : str
            Dowolny tekst

        Wyjątki
        -------
        InvalidCurrency
            Wyrzucany w przypadku nie odnalezienia waluty o podanej nazwie
    """
    text = text.split(' czy ')
    if len(text) == 1:
        raise exc.OnlyOneCurrency
    first_currency = ''
    second_currency = ''

    first_to_check = text[0].split()
    first_to_check.reverse()
    for element in first_to_check:
        first_currency = element + first_currency
        if first_currency in SPECIAL_A_TABLE_CURRENCIES or first_currency in A_TABLE_CURRENCIES or \
                first_currency in B_TABLE_CURRENCIES:
            break
        first_currency = ' ' + first_currency

    if first_currency not in A_TABLE_CURRENCIES and first_currency not in B_TABLE_CURRENCIES:
        first_currency = ''
        for element in first_to_check:
            first_currency = element + first_currency
            if first_currency in SPECIAL_A_TABLE_CURRENCIES:
                break
            first_currency = ' ' + first_currency

        if first_currency not in SPECIAL_A_TABLE_CURRENCIES and first_currency not in A_TABLE_CURRENCIES and \
                first_currency not in B_TABLE_CURRENCIES:
            raise exc.InvalidCurrency

    for element in text[1].split():
        second_currency += element
        if second_currency in A_TABLE_CURRENCIES or second_currency in B_TABLE_CURRENCIES:
            break
        second_currency += ' '

    if second_currency not in A_TABLE_CURRENCIES and second_currency not in B_TABLE_CURRENCIES:
        second_currency = ''
        for element in text[1].split():
            second_currency += element
            if SPECIAL_A_TABLE_CURRENCIES:
                break
            second_currency += ' '

        if second_currency not in SPECIAL_A_TABLE_CURRENCIES and second_currency not in A_TABLE_CURRENCIES and \
                second_currency not in B_TABLE_CURRENCIES:
            raise exc.InvalidCurrency

    return [first_currency, second_currency]


def compare_currencies(currencies, rate, date='/', higher=True):
    """ Funkcja porównująca kursy dwóch walut. Zwraca informacje o tym który kurs był większy lub mniejszy w zależności
        od podanych argumentów

        Argumenty
        ---------
        currencies : list
            Lista zawierająca dwie nazwy walut do porównania
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
        date : str, opcjonalny
            Data w postaci ciągu znaków, domyślna wartość to '/' oznaczająca aktualny kurs
        higher : bool, opcjonalny
            Argument określający jaki kurs interesuje użytkownika większy czy mniejszy. Domyślna wartość True oznacza,
            kurs większy
    """
    first_currency_value = get_exchange_rate_single_currency(currencies[0], rate, date)
    second_currency_value = get_exchange_rate_single_currency(currencies[1], rate, date)
    if higher:
        if first_currency_value > second_currency_value:
            return currencies[0]
        elif first_currency_value < second_currency_value:
            return currencies[1]
        else:
            return 'równe'
    else:
        if first_currency_value < second_currency_value:
            return currencies[0]
        elif first_currency_value > second_currency_value:
            return currencies[1]
        else:
            return 'równe'


def compare_currencies_response(currencies, rate, date='/', higher=True):
    """ Funkcja zwraca informację o porównaniu dwóch kursów na podstawie argumentów

        Argumenty
        ---------
        currencies : list
            Lista zawierająca dwie nazwy walut do porównania
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
        date : str, opcjonalny
            Data w postaci ciągu znaków, domyślna wartość to '/' oznaczająca aktualny kurs
        higher : bool, opcjonalny
            Argument określający jaki kurs interesuje użytkownika większy czy mniejszy. Domyślna wartość True oznacza,
            kurs większy
    """
    currency = compare_currencies(currencies, rate, date, higher)
    if rate == 'mid':
        rate = 'średni kurs'
    elif rate == 'bid':
        rate = 'kurs kupna'
    else:
        rate = 'kurs sprzedaży'

    if date == '/':
        start = rate
        time = 'jest'
    else:
        start = 'Dnia ' + date + ' ' + rate
        time = 'był'

    if higher:
        compare = 'większy'
    else:
        compare = 'mniejszy'

    if currency == 'równe':
        return start + ' ' + currencies[0] + ' i ' + currencies[1] + ' ' + time + ' taki sam'
    else:
        return start + ' ' + currency + ' ' + time + ' ' + compare


def get_best_date(currency, rate, date_from, date_to, best=True):
    """ Funkcja zwracająca dzień w którym kurs był największym lub najmniejszym w podanym przedziale czasowym

        Argumenty
        ---------
        currency : str
            Nazwa wybranej waluty
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
        date_from : str
            Data w postaci ciągu znaków od której mają zostać pobrane dane
        date_to : str
            Data w postaci ciągu znaków do której mają zostać pobrane dane
        best : bool, opcjonalny
            Argument określający czy szukać największego czy najmniejszego kursu w podanym przedziale czasowym.
            Domyślna wartość True określa nawiększy kurs
    """
    table, currency_code = find_table_and_rate(currency, rate)
    currency_data = get_api_response(table, currency_code, date_from, date_to)
    chosen_day = ''

    if best:
        value = 0
    else:
        value = 10000

    for rates in currency_data['rates']:
        if (best and rates[rate] > value) or (not best and rates[rate] < value):
            value = rates[rate]
            chosen_day = rates['effectiveDate']

    return chosen_day


def get_single_currency_from_query(query):
    """ Funkcja do pobrania nazwy waluty z zapytania

        Argumenty
        ---------
        query : str
            Dowolne zapytanie

        Wyjątki
        -------
        InvalidCurrency
            Wyrzucany w przypadku nie odnalezienia waluty o podanej nazwie
    """
    for curr in A_TABLE_CURRENCIES:
        if curr in query:
            return curr

    for curr in B_TABLE_CURRENCIES:
        if curr in query:
            return curr

    for curr in SPECIAL_A_TABLE_CURRENCIES:
        if curr in query:
            return curr

    raise exc.InvalidCurrency


def get_best_date_response(currency, rate, date_from, date_to, time, time_unit, best=True):
    """ Funkcja zwracająca informację o największym lub najmniejszym kursie w podanym przedziale czasowym w zależności
        od podanych argumentów

        Argumenty
        ---------
        currency : str
            Nazwa waluty
        rate : str
            Jedna z wartości:
            'mid' - średni kurs
            'bid' - kurs kupna
            'ask' - kurs sprzedaży
        date_from : str
            Data w postaci ciągu znaków od której mają zostać pobrane dane
        date_to : str
            Data w postaci ciągu znaków do której mają zostać pobrane dane
        time : str
            Miesiąc lub rok
        time_unit : int
            0 jeżeli spradzany jest obecny miesiąc/rok, -1 jeżeli sprawdzany jest poprzedni miesiąc/rok
        best : bool, opcjonalny
            Argument określający czy szukać największego czy najmniejszego kursu w podanym przedziale czasowym.
            Domyślna wartość True określa nawiększy kurs
    """
    day_to_return = get_best_date(currency, rate, date_from, date_to, best)
    if best:
        best = 'największy'
    else:
        best = 'najmniejszy'

    if time_unit == 0:
        time_unit = 'tym'
    else:
        time_unit = 'zeszłym'

    return 'W ' + time_unit + ' ' + time + ' kurs ' + currency + ' był ' + best + ' dnia ' + day_to_return


def prepare_answer(query):
    """ Funkcja do przetwarzania zapytania i zwracania odpowiedniej odpowiedzi

        Argumenty
        ---------
        query : str
            Dowolne zapytanie
    """
    query = query.lower()
    try:
        if 'kurs' in query:
            if 'kupna' in query:
                rate = 'bid'
                rate_sep = 'kurs kupna '
            elif 'sprzedaży' in query:
                rate = 'ask'
                rate_sep = 'kurs sprzedaży '
            else:
                rate_sep = 'kurs '
                rate = 'mid'
                if 'średni' in query:
                    rate_sep = 'średni kurs '

            query_split = query.split(rate_sep)
            if len(query_split) == 2:
                check = query_split[0]
                check = check.rstrip()
                if check in ['jaki jest teraźniejszy', 'jaki jest', 'jaki jest obecny', 'jaki jest bieżący',
                             'jaki jest dzisiejszy', 'podaj', 'podaj teraźniejszy', 'podaj obecny',
                             'podaj dzisiejszy', 'podaj bieżący', 'jaki jest aktualny', 'podaj aktualny']:
                    currencies = get_currencies_from_text(query_split[1])
                    return get_current_exchange_rate_response(currencies, rate)

                if check in ['jaki był', 'ile wynosił', 'jaką miał wartość']:
                    currencies = get_currencies_from_text(query_split[1])
                    return get_exchange_rate_by_date_response(currencies, query_split[1], rate)

                if check in ['jak zmienił się']:
                    currencies = get_currencies_from_text(query_split[1])
                    return get_difference_between_dates_response(query_split[1], currencies, rate)

                if 'największy' in query or 'najmniejszy' in query or 'najlepszy' in query or 'najgorszy' in query \
                        or 'najwyższy' in query or 'najniższy' in query:
                    add_value = None
                    if 'największy' in query or 'najlepszy' in query or 'najwyższy' in query:
                        best = True
                    else:
                        best = False

                    if 'w zeszłym' in query or 'zeszłego' in query or 'poprzedniego' in query or 'w poprzednim' in query or 'w ostatnim' in query or 'ostatniego':
                        add_value = -1

                    if 'tego' in query or 'w tym' in query:
                        add_value = 0

                    if ('miesiąca' in query or 'miesiącu' in query) and add_value is not None:
                        current_date = date.today() + relativedelta(months=add_value)
                        start_date = current_date.strftime('%Y-%m-%d')[:-2] + '01'
                        end_date = current_date.strftime('%Y-%m-%d')
                        if add_value == -1:
                            end_date = end_date[:-2] + str(
                                calendar.monthrange(current_date.year, current_date.month)[1])

                        currency = get_single_currency_from_query(query)
                        return get_best_date_response(currency, rate, start_date, end_date, 'miesiącu', add_value, best)

                    if 'roku' in query and add_value is not None:
                        current_date = date.today() + relativedelta(years=add_value)
                        start_date = current_date.strftime('%Y-%m-%d')[:-5] + '01-01'
                        end_date = current_date.strftime('%Y-%m-%d')
                        if add_value == -1:
                            end_date = end_date[:-5] + '12-31'

                        currency = get_single_currency_from_query(query)
                        return get_best_date_response(currency, rate, start_date, end_date, 'roku', add_value, best)

                if 'większy' in query_split[1] or 'mniejszy' in query_split[1]:
                    if 'większy' in query_split[1]:
                        higher = True
                    else:
                        higher = False

                    currencies = get_currencies_to_compare(query_split[1])
                    if 'jest' in query_split[1]:
                        return compare_currencies_response(currencies, rate, higher=higher)

                    elif 'był' in query_split[1]:
                        date_to_check = get_date_from_text(query_split[1])
                        return compare_currencies_response(currencies, rate, date=date_to_check, higher=higher)

        if 'kod' in query:
            if 'jaki' in query or 'podaj' in query:
                return get_code_by_currency(query)

            if 'która' in query:
                return get_currency_by_code(query)

        return None

    except exc.NotFoundException:
        return 'Nie posiadam takich informacji'
    except exc.InvalidDateException:
        return 'Podano nieprawidłową datę'

    except exc.InvalidCurrency:
        return 'Nie znam takiej waluty'

    except exc.MissingDate:
        return 'Podano niepełną datę. Proszę podać dzień, miesiąc oraz rok'

    except exc.OnlyOneCurrency:
        return 'Proszę podać dwie waluty, dla których mam podać kurs'

    except exc.CodeNotFound:
        return 'Nie znaleziono waluty o takim kodzie'


if __name__ == '__main__':
    pass
