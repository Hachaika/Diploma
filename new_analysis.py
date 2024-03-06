import json
from datetime import datetime
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

            # Извлечь статус события
            status_name = event.get('status', {}).get('name')

            # Пропустить событие, если статус "Rejected" или время выполнения задания равно 0
            if status_name == 'Rejected' or event.get('spent_hours', 0) == 0:
                continue

            # Добавить участников события в уникальный набор, если имя не пустое
            assigned_to_name = event.get('assigned_to', {}).get('name')
            if assigned_to_name:
                unique_people.add(assigned_to_name)

            timeline.append({
                'ID задания': event.get('id', 'N/A'),
                'Дата создания': start_date,
                'Дата закрытия': end_date,
                'Сложность в SP': event.get('sp', 'N/A'),
                'Приоритет': event.get('priority', {}).get('name', 'Без приоритета'),
                'Потрачено времени в часах': event.get('spent_hours', 0),
                'Участник': assigned_to_name
            })

    return timeline, unique_people


def parse_datetime(date_string):
    if date_string is None:
        return None
    return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z').replace(tzinfo=None) if date_string else None


# путь к файлу JSON
json_path = 'C:/Users/vippo/OneDrive/Рабочий стол/diploma/all_redmine_tasks.json'

with open(json_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Фильтрация задач, созданных после 2022-12-31
filtered_data = [event for event in data if 'created_on' in event and parse_datetime(event['created_on'])]

# Обработка событий
timeline, unique_people = process_events(filtered_data)

# Преобразование данных в DataFrame
df = pd.DataFrame(timeline)

# Замена пустых значений приоритета на "Без приоритета"
df['Приоритет'].fillna('Без приоритета', inplace=True)

# Округление значений
df['Потрачено времени в часах'] = df['Потрачено времени в часах'].round(2)

# Вывод распределения времени выполнения задач и их количества по приоритетам и типам в SP
priority_sp_stats = df.groupby(['Приоритет', 'Сложность в SP']).agg({'Потрачено времени в часах': 'mean'}).reset_index()
priority_sp_stats.columns = ['Приоритет', 'Сложность в SP', 'Среднее время выполнения в часах']
priority_sp_stats['Среднее время выполнения в часах'] = priority_sp_stats['Среднее время выполнения в часах'].round(2)


# Создание таблицы с участниками и их статистикой по типам заданий
participants_table = pd.DataFrame(columns=['Участник'])

# Inside the loop:
participant_tables = []

for person in unique_people:
    person_data = df[df['Участник'] == person].copy()  # Ensure a copy of the DataFrame

    # Группировка данных по участникам, приоритету, сложности и типу задания
    grouped_data = person_data.groupby(['Участник', 'Приоритет', 'Сложность в SP']).agg({'Потрачено времени в часах':
                                                                                             'mean'}).reset_index()
    # Округление значений до двух знаков
    grouped_data['Потрачено времени в часах'] = grouped_data['Потрачено времени в часах'].round(2)

    # Добавление столбца с типом задания (вида "P*_SP*")
    grouped_data['Тип задания'] = grouped_data.apply(lambda row: f"{row['Приоритет']}_SP{row['Сложность в SP']}", axis=1)

    # Группировка данных по участникам и типу задания
    participant_stats = grouped_data.groupby(['Участник', 'Тип задания']).agg({'Потрачено времени в часах':
                                                                                   'mean'}).reset_index()

    # Фильтрация строк, где 'Потрачено времени в часах' не равно 0
    participant_stats = participant_stats.loc[participant_stats['Потрачено времени в часах'] != 0]

    # Округление значений до двух знаков
    participant_stats['Потрачено времени в часах'] = participant_stats['Потрачено времени в часах'].round(2)

    # Подготовка таблицы participants_stats
    participants_stats = participant_stats.pivot_table(index='Участник', columns='Тип задания',
                                                       values='Потрачено времени в часах', fill_value=0)

    # Добавление столбца с именем участника
    participants_stats['Участник'] = participants_stats.index

    # Перемещение столбца с именем участника в начало таблицы
    participants_stats = participants_stats[
        ['Участник'] + [col for col in participants_stats.columns if col != 'Участник']]

    # Append the person's statistics to the list of participant tables
    participant_tables.append(participants_stats)

# Concatenate all participant tables into a single DataFrame
participants_table = pd.concat(participant_tables, ignore_index=True)

# Рассчитываем среднее время выполнения задания для каждого участника и каждого типа задания
average_time_per_person_and_task_type = participants_table.copy()

# Удаляем столбец с именем участника для расчета среднего
average_time_per_person_and_task_type.drop(columns=['Участник'], inplace=True)

# Рассчитываем среднее время выполнения задания для каждого типа задания
average_time_per_task_type = average_time_per_person_and_task_type.mean()

# Добавляем столбик КПД в participants_table
for task_type in average_time_per_task_type.index:
    participants_table[f'KPD_{task_type}'] = participants_table[task_type] / average_time_per_task_type[task_type]

# Рассчитываем среднее значение по всем столбцам КПД для каждого пользователя
participants_table['Total_KPD'] = participants_table.filter(like='KPD').mean(axis=1)

# Округление значений до двух знаков
participants_table['Total_KPD'] = participants_table['Total_KPD'].round(2)

# Сохранение данных в файл Excel
excel_path = 'results.xlsx'
with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
    df.to_excel(writer, sheet_name='timeline_data', index=False)
    priority_sp_stats.to_excel(writer, sheet_name='priority_sp_stats', index=False)
    unique_people_df = pd.DataFrame(list(unique_people), columns=['Участники'])
    unique_people_df.to_excel(writer, sheet_name='unique_people', index=False)
    participants_table.to_excel(writer, sheet_name='participants_stats', index=False)

print(f"Данные сохранены в {excel_path}")

