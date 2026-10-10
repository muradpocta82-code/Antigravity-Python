import sqlite3
import pandas as pd

# Имитируем входящую пачку документов
documents_batch = [
    {
        'doc_id': 'ЖД-101',
        'sender': 'ООО "ТехноПром", г. Москва',
        'vagon_number': '52890144',
        'weight_tons': 45,
        'status': 'ОК',
    },
    {
        'doc_id': 'ЖД-102',
        'sender': 'ЗАО "УралСтиль", г. Екатеринбург',
        'vagon_number': '77120931',
        'weight_tons': 60,
        'status': 'ОК',
    },
    {
        'doc_id': 'ЖД-103',
        'sender': 'ООО "ЛогистикГрупп", г. Казань',
        'vagon_number': 'НЕ УКАЗАН',
        'weight_tons': 30,
        'status': 'Ошибка',
    },
    {
        'doc_id': 'ЖД-104',
        'sender': 'ИП Иванов, г. Самара',
        'vagon_number': '99310245',
        'weight_tons': 15,
        'status': 'ОК',
    },
]

# Превращаем в датафрейм
df = pd.DataFrame(documents_batch)

# 1. ПОДКЛЮЧАЕМСЯ К БАЗЕ ДАННЫХ SQLite (она создастся сама в файле railway.db)
conn = sqlite3.connect('railway.db')
cursor = conn.cursor()

# 2. ЗАПИСЫВАЕМ ТАБЛИЦУ В БАЗУ ДАННЫХ (в табличку 'shipments')
df.to_sql('shipments', conn, if_exists='replace', index=False)
print(
    '=== 1. ДАННЫЕ УСПЕШНО ЗАПИСАНЫ В БАЗУ ДАННЫХ (railway.db) ===\n'
)  # 3. ДЕЛАЕМ SQL-ЗАПРОСЫ (как на реальной работе!)

# Запрос А: Выбрать только те накладные, где статус 'ОК' и вес больше 40 тонн
query_ok = """
    SELECT doc_id, sender, weight_tons 
    FROM shipments 
    WHERE status = 'ОК' AND weight_tons > 40
"""
result_ok = pd.read_sql(query_ok, conn)

print('=== 2. РЕЗУЛЬТАТ SQL-ЗАПРОСА (Крупные отправки со статусом ОК) ===')
print(result_ok, '\n')

# Запрос Б: Посчитать общий вес по всей базе через SQL-функцию SUM()
query_sum = 'SELECT SUM(weight_tons) as total_weight FROM shipments'
total_weight = pd.read_sql(query_sum, conn).iloc[0]['total_weight']

print(f'=== 3. СУММАРНЫЙ ВЕС ИЗ БАЗЫ ДАННЫХ: {total_weight} тонн ===')

# Закрываем соединение с базой
conn.close()