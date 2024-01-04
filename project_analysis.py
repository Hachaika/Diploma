import json
from datetime import datetime, timedelta
import pandas as pd


def process_events(events):
    timeline = []
    unique_people = set()

    for event in events:
        if 'created_on' in event and 'closed_on' in event:
            start_date = parse_datetime(event['created_on'])
            end_date = parse_datetime(event['closed_on'])

            # Пропускать событие, если start_date или end_date равны None
            if start_date is None or end_date is None:
                continue

            # Подсчитать количество повторных открытий
            reopenings = 1 if event.get('status', {}).get('name') == 'Re-opened' else 0
            days_to_complete = (end_date - start_date).days

            # Добавить участников события в уникальный набор
            unique_people.add(event.get('author', {}).get('name', 'N/A'))
            unique_people.add(event.get('assigned_to', {}).get('name', 'N/A'))

            timeline.append({
                'ID задания': event.get('id', 'N/A'),
                'Дата создания': start_date,
                'Дата закрытия': end_date,
                'Сложность в SP': event.get('sp', 'N/A'),
                'Приоритет': event.get('priority', {}).get('name', 'Без приоритета'),
                'Кол-во переоткрытий': reopenings,
                'Дни на выполнение': days_to_complete,
                'Потрачено времени в часах': event.get('spent_hours', 0),
            })

    return timeline, unique_people


def parse_datetime(date_string):
    if date_string is None:
        return None
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None) if date_string else None


# Здесь нужно указать путь к вашему файлу JSON
json_path = 'C:/Users/vippo/OneDrive/Рабочий стол/diploma/all_redmine_tasks.json'

with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Фильтрация задач, созданных после 2022-12-31
filtered_data = [event for event in data if 'created_on' in event and parse_datetime(event['created_on']).year >= 2023]

# Обработка событий
timeline, unique_people = process_events(filtered_data)

# Преобразование данных в DataFrame
df = pd.DataFrame(timeline)

# Замена пустых значений приоритета на "Без приоритета"
df['Приоритет'].fillna('Без приоритета', inplace=True)

# Округление значений
df['Потрачено времени в часах'] = df['Потрачено времени в часах'].round(2)

# Сохранение в файл Excel
excel_path = 'C:/Users/vippo/OneDrive/Рабочий стол/diploma/all_tables.xlsx'
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='timeline_data', index=False)

    # Вывод общего количества участников проекта
    unique_people_df = pd.DataFrame(list(unique_people), columns=['Участники'])
    unique_people_df.to_excel(writer, sheet_name='unique_people', index=False)

    # Вывод распределения времени выполнения задач и их количества по приоритетам
    priority_distribution = df.groupby('Приоритет').agg({'Дни на выполнение': ['count', 'mean']}).reset_index()
    priority_distribution.columns = ['Приоритет', 'Количество задач', 'Среднее время выполнения в днях']
    priority_distribution['Среднее время выполнения в днях'] = priority_distribution[
        'Среднее время выполнения в днях'].round(0)
    priority_distribution.to_excel(writer, sheet_name='priority_distribution', index=False)

    # Вывод распределения времени выполнения задач и их количества по сложности в SP
    story_points_stats = df.groupby('Сложность в SP').agg({'Дни на выполнение': ['count', 'mean'],
                                                           'Потрачено времени в часах': ['sum', 'mean']}).reset_index()
    story_points_stats.columns = ['Сложность в SP', 'Количество задач', 'Среднее время выполнения в днях',
                                  'Потрачено времени в часах', 'Среднее потраченное время в часах на задание']
    story_points_stats['Среднее время выполнения в днях'] = story_points_stats['Среднее время выполнения в днях'].round(0)
    story_points_stats['Потрачено времени в часах'] = story_points_stats['Потрачено времени в часах'].round(2)
    story_points_stats['Среднее потраченное время в часах на задание'] = story_points_stats[
        'Среднее потраченное время в часах на задание'].round(2)
    story_points_stats.to_excel(writer, sheet_name='story_points_stats', index=False)

    # Вывод общей таблицы с распределением приоритетам по SP и временем выполнения
    total_table = df.groupby(['Приоритет', 'Сложность в SP']).agg(
        {'Дни на выполнение': ['count', 'mean'],
         'Потрачено времени в часах': ['sum', 'mean']}).reset_index()
    total_table.columns = ['Приоритет', 'Сложность в SP', 'Количество задач', 'Среднее время выполнения в днях',
                           'Потрачено времени в часах', 'Среднее потраченное время в часах на задание']
    total_table['Среднее время выполнения в днях'] = total_table['Среднее время выполнения в днях'].round(0)
    total_table['Потрачено времени в часах'] = total_table['Потрачено времени в часах'].round(2)
    total_table['Среднее потраченное время в часах на задание'] = total_table[
        'Среднее потраченное время в часах на задание'].round(2)
    total_table.to_excel(writer, sheet_name='total_table', index=False)

    # Вывод таблицы с заданиями, у которых значения spent_hours и total_spent_hours не равны 0
    table_with_spent_hours = df[(df['Потрачено времени в часах'] != 0)]
    table_with_spent_hours.to_excel(writer, sheet_name='table_with_spent_hours', index=False)

print(f"Данные сохранены в {excel_path}")
