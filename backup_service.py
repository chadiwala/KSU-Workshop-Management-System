import csv
from pathlib import Path
from booking_service import get_connection


def backup_database(folder='backup'):
    output = Path(folder)
    output.mkdir(parents=True, exist_ok=True)
    with get_connection() as connection:
        for table in ('students', 'admins', 'workshops', 'bookings'):
            cursor = connection.execute('SELECT * FROM ' + table)
            columns = [column[0] for column in cursor.description]
            with (output / (table + '.csv')).open('w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(cursor.fetchall())
    return str(output.resolve())


if __name__ == '__main__':
    print('Backup saved in:', backup_database())
