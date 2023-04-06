import main
import random
import pymorphy2
import database
from itertools import product

# Рандомная выборка count категорий из списка
def sample_of_categories(count):
    categories = main.get_categories()
    return random.sample( categories, count )

# Класс для морфологического разбора
morph = pymorphy2.MorphAnalyzer()
def get_single_and_plural_numbers(word):
    try:
        # Получаем единственное число
        single = morph.parse(word)[0].inflect({'sing'}).word

        # Получаем множественное число
        plural = morph.parse(word)[0].inflect({'plur'}).word
        return single, plural
    except: return (word, )

def different_ways_to_perephrase_the_category(category):
    # Если название состоит из одного слова, то в именительный падеж
    if ' ' not in category: category = morph.parse(category)[0].inflect({'nomn'}).word
    words = category.split()
    words = [ get_single_and_plural_numbers(word) for word in words]
    combinations = list(product(*words))
    return list(map(lambda combination: ' '.join(combination), combinations))

def find_the_best_normalize_way(ways):
    statistics = { way: main.total_count(way) for way in ways}
    statistics = {k: v for k, v in sorted(statistics.items(), key=lambda item: item[1])[::-1]}
    key = next(iter(statistics)); value = statistics[key]
    return key, value

def normalize_category(category, request_count):
    ways = different_ways_to_perephrase_the_category(category)
    normalize = find_the_best_normalize_way(ways)
    if normalize[1] <= request_count: normalize = (category, request_count)
    return normalize
    # database.add_record_to_pymorph(category=category, request_count=request_count, normalize_category=normalize[0],
    #                                normalize_request_count=normalize[1])

def test():
    # Рандомные 100 категорий
    random_categories = sample_of_categories(100)
    for category in random_categories:
        try:
            request_count = main.total_count(category)
            thread = main.Thread(target=normalize_category, args=(category, request_count))
            thread.start()
            # normalize_category(category)
        except:
            print( f'https://trending-searches.wb.ru/api?itemsPerPage=1000000&offset=0&period=week&query={category}' )


if __name__ == '__main__':
    # test()
    print(
        normalize_category('Сухие напитки', 10)
    )