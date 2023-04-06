import requests # модуль для запросов к WildBerries
import database # собственный модуль для работы с БД
import json
from threading import Thread
import test # собственный модуль для тестов


# Возвращает список категорий
def get_categories():
    with open('categories.json', encoding='UTF-8') as categories_file:
        return list(map(lambda x: x['objectName'], json.load(categories_file)['data']))

def total_count(category):
    URL = f'https://trending-searches.wb.ru/api?itemsPerPage=1000000&offset=0&period=week&query={category}'
    json = requests.get(URL).json()
    return sum([ record['requestCount'] for record in json['data']['list'] ])

# Проверяет товар на наличие (передавать его ID из json)
def is_available(good_id):
    URL = f'https://card.wb.ru/cards/list?&nm={good_id}'
    json = requests.get(URL).json()
    return json['data']['products'] != []

# Найти cpm по первым 4-м рекламам
def find_cpms(category, json):
    cpms = []
    if json['adverts'] != None:
        prioritySubject = json['prioritySubjects'][0]
        for good in json['adverts']:
            if is_available(good['id']) and good['subject'] == prioritySubject:
                cpms.append(good['cpm'])
                if len(cpms) >= 4: break

    return cpms

def find_average_price(category):
    URL = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={category}&reg=0&regions=80,64,83,4,38,33,70,68,69,86,75,30,40,48,1,66,31,22,71&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false'
    json = requests.get(URL).json()
    prices = [product['salePriceU'] // 100 for product in json['data']['products'][:10]]
    return sum(prices)/len(prices) # средняя цена

def find_amount(category):
    URL = f'https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&couponsGeo=12,3,18,15,21&curr=rub&dest=-1029256,-102269,-2162196,-1257786&emp=0&lang=ru&locale=ru&pricemarginCoeff=1.0&query={category}&reg=0&regions=80,64,83,4,38,33,70,68,69,86,75,30,40,48,1,66,31,22,71&resultset=filters&spp=0&suppressSpellcheck=false'
    json = requests.get(URL).json()
    return json['data']['total']

threads = 0 # кол-во потоков, выполняемых в настоящий момент
# Анализирует категорию, возвращая словарь с нужными столбцами для записи в БД
def analyze_category(category):
    global threads
    try:
        threads += 1
        URL = f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={category}'
        json = requests.get(URL).json() # получили json
        total_count_in_category = total_count(category) # общее кол-во запросов по категории
        normalize = test.normalize_category(category, total_count_in_category)
        cpms = find_cpms(normalize[0], json) # первые 4 cpms рекламные ставки
        average_price = find_average_price(normalize[0]) # первые 4 цены в категории
        amount = find_amount(normalize[0]) # кол-во товаров в категории

        # Добавление собранных сведений в БД
        database.add_record_to_parser(cpms=cpms, normalize_category=normalize[0], average_price=average_price, amount_of_goods=amount, category=category, total_count=normalize[1])
        print(f'[{category}] Анализ завершён!. Потоков: {threads}')
    except:
        pass
    finally:
        threads -= 1


def start_parse():
    categories = get_categories() # берём список всех категорий
    database.clear_table() # очищаем таблицу перед запуском парсера
    for category in categories:
        try:
            while (threads >= 50): pass # Ждём, пока потоков станет не меньше 10-ти
            # создаём поток, анализирующий каждую категорию в отдельности
            thread = Thread(target=analyze_category, args=(category, ))
            thread.start()
            # analyze_category(category) # это обычный-медленный анализ, не многопоточный
        except: pass

# Если программа запущена напрямую, то вызываем главную функцию
if __name__ == '__main__':
    start_parse()
