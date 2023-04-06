# WildBerriesParser - извлекаем 7400 категорий за 8 минут
[Парсер] Автоматический сбор информации с крупнейшего маркетплейса РФ и последующая выгрузка её в БД

В рамках заказа от ~~*одной небезызвестной компании*~~ пришлось написать парсер, который бы собирал информацию по 7400+ категориям товаров на WildBerries и затем выгружал в удалённую базу данных MySQL
Схема такова: по каждой интересующей категории выдёргиваем JSON и получаем следующую информацию:
1) Название категории
2) Нормализованное название (бывает такое, что названия склоняют по падежам, и от этого меняется количество выданных товаров, что неэффективно. Отдельная же моя функция
анализирует всевозможные склонения и выбирает тот, при котором количество выданных товаров наибольшее)
3) Количество товаров в данной категории
4) Количество запросов в месяц (таким образом можно проверить ликвидность товара на рынке)
5) Средняя цена за ТОП-3 товара в этой категории (3 первые карточки на странице выдачи)
6) ТОП-4 Рекламные ставки, которые платят продавцы WildBerries за нахождение на первых позициях в поиске (это бизнес, детка!)

## Выглядит это в БД примерно так:
![Записи категорий в БД](https://github.com/OYBOLATOFF/WildBerriesParser/blob/main/example.jpg)
