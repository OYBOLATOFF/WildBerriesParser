from mysql.connector import connect
from datetime import datetime



def add_record_to_parser(cpms, average_price, amount_of_goods, category, total_count, normalize_category):
    amount_of_goods = 0 if amount_of_goods == '' else amount_of_goods
    connection = connect(host='localhost', user='root', password='Decadance313')
    cursor = connection.cursor()
    if cpms == []: cpms = [0, 0, 0, 0]
    if len(cpms) < 4: cpms += [0] * (4 - len(cpms)) # если не нашлось 4 cpm показателя, то во избежания ошибки при SQL запросе дописываем недостающие нули
    command = f"INSERT INTO parser_for_ignat.parser(category, normalize_category, amount_of_goods, amount_of_requests, average_price, rate_1, rate_2, rate_3, rate_4) VALUES ('{category}', '{normalize_category}', {amount_of_goods}, {total_count}, {average_price}, {cpms[0]}, {cpms[1]}, {cpms[2]}, {cpms[3]})"
    cursor.execute(command)

    connection.commit()

def clear_table():
    connection = connect(host='localhost', user='root', password='Decadance313')
    cursor = connection.cursor()
    cursor.execute('TRUNCATE TABLE parser_for_ignat.parser')
    connection.commit()

def add_record_to_pymorph(category, request_count, normalize_category, normalize_request_count):
    with connect(host='localhost', user='root', password='Decadance313') as connection:
        cursor = connection.cursor()
        command = f"INSERT INTO parser_for_ignat.pymorph(category, request_count, normalize_category, normalize_request_count) VALUES ('{category}', {request_count}, '{normalize_category}', {normalize_request_count})"
        cursor.execute(command)

        connection.commit()

def main():
    pass


if __name__ == '__main__':
    main()
