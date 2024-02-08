from celery import shared_task
import requests
from telecom.models import Operator, PhoneNumber
import csv
from pathlib import Path

@shared_task
def load_data_from_csv_task():
    urls = [
        'https://opendata.digital.gov.ru/downloads/ABC-3xx.csv?1662393366550',
        'https://opendata.digital.gov.ru/downloads/ABC-4xx.csv?1662393366550',
        'https://opendata.digital.gov.ru/downloads/ABC-8xx.csv?1662393366551',
        'https://opendata.digital.gov.ru/downloads/DEF-9xx.csv?1662393366551',
    ]

    for url in urls:
        response = requests.get(url, verify=False)
        if response.status_code == 200:
            file_path = Path('temp.csv')
            file_path.write_bytes(response.content)

            with open(file_path, mode='r', encoding='utf-8-sig') as file:
                reader = csv.reader(file, delimiter=';')
                next(reader)  # Пропускаем заголовок
                for row in reader:
                    if len(row) != 7:
                        print(f'Некорректное количество столбцов в строке: {row}')
                        continue
                    operator, _ = Operator.objects.get_or_create(name=row[4], inn=row[6])
                    PhoneNumber.objects.update_or_create(
                        code=int(row[0]),
                        start_range=int(row[1]),
                        end_range=int(row[2]),
                        defaults={
                            'capacity': int(row[3]),
                            'operator': operator,
                            'region': row[5]
                        }
                    )
            file_path.unlink()
            print(f'База номеров успешно обновлена из {url}')
        else:
            print(f'Ошибка загрузки файла с URL: {url}')
