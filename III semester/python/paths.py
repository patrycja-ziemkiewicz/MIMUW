import argparse
import os
import random
import csv
import json


def create_days_dictionary():
    days = {
        'pn': 'poniedziałek',
        'wt': 'wtorek',
        'śr': 'środa',
        'cz': 'czwartek',
        'pt': 'piątek',
        'sb': 'sobota',
        'nd': 'niedziela'
    }
    return days


def get_days_range(start, end, days_dictionary):
    days_keys = list(days_dictionary.keys())
    start_id = days_keys.index(start)
    end_id = days_keys.index(end)
    return days_keys[start_id: end_id + 1]


def create_CSV_file(direction_path):
    file_name = 'Dane.csv'
    file_path = os.path.join(direction_path, file_name)
    if os.path.exists(file_path):
        print(f'CSV file already exists: {file_path}')
    else:
        header = ['Model', 'Wynik', 'Czas']
        with open(file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(header)
            model = random.choice(['A', 'B', 'C'])
            output_value = random.randint(0, 1000)
            time_of_computation = f'{random.randint(0, 1000)}s'
            writer.writerow([model, output_value, time_of_computation])
            print(f'CSV file created: {file_path}')


def read_CSV_file(direction_path):
    file_name = 'Dane.csv'
    file_path = os.path.join(direction_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file, delimiter=';')  # Reader creates dictionary, where keys are from header.
            for row in reader:
                if row['Model'] == 'A':
                    time_of_computation = row['Czas']
                    time_of_computation = int(time_of_computation[:-1])  # Removes s and changes to integer.
                    return time_of_computation
                else:
                    return 0
    else:
        print(f"CSV file doesn't exist: {file_path}")
        return 0


def create_JSON_file(direction_path):
    file_name = 'Dane.json'
    file_path = os.path.join(direction_path, file_name)
    if os.path.exists(file_path):
        print(f'JSON file already exists: {file_path}')
    else:
        with open(file_path, 'w', newline='') as file:
            data = {
                'Model': random.choice(['A', 'B', 'C']),
                'Wynik': random.randint(0, 1000),
                'Czas': f'{random.randint(0, 1000)}s'
            }
            json.dump(data, file)
            print(f'JSON file created: {file_path}')


def read_JSON_file(direction_path):
    file_name = 'Dane.json'
    file_path = os.path.join(direction_path, file_name)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            if data['Model'] == 'A':
                time_of_computation = int((data['Czas'])[:-1])
                return time_of_computation
            else:
                return 0
    else:
        print(f"JSON file doesn't exist: {file_path}")
        return 0


def create_directories(months, days, times, days_dictionary, times_dictionary, t, c, j):
    sum_csv = 0
    sum_json = 0
    for month, days_range in zip(months, days):
        days_split = days_range.split('-')
        days_split = get_days_range(days_split[0], days_split[len(days_split) - 1], days_dictionary)
        for day in days_split:
            if not times:
                direction_path = os.path.join(os.getcwd(), month, days_dictionary[day], times_dictionary['r'])
            else:
                direction_path = os.path.join(os.getcwd(), month, days_dictionary[day], times_dictionary[times[0]])
                del times[0]
            if not c and not j:
                if t and os.path.exists(direction_path):
                    print(f'Path already exists: {direction_path}')
                elif not t and not os.path.exists(direction_path):
                    print(f"Path doesn't exist: {direction_path}")
            if t and not os.path.exists(direction_path):
                os.makedirs(direction_path)
            if c and t:
                create_CSV_file(direction_path)
            if c and not t:
                sum_csv += read_CSV_file(direction_path)
            if j and t:
                create_JSON_file(direction_path)
            if j and not t:
                sum_json += read_JSON_file(direction_path)
    if c and not t:
        print(f'Sum of times for model A in .csv files is: {sum_csv}s')
    if j and not t:
        print(f'Sum of times for model A in .json files is: {sum_json}s')


def main():
    days_dictionary = create_days_dictionary()
    times_dictionary = {'r': 'rano', 'w': 'wieczorem'}

    parser = argparse.ArgumentParser()

    parser.add_argument('--months', nargs="+", required=True, help='List of months to include (e.g., styczeĹ„, luty)')
    parser.add_argument('--days', nargs="+", required=True, help='List of day ranges (e.g., pn-wt, pt)')
    parser.add_argument('--times', nargs="*", help="List of times in a day ('r' or 'w')")

    parser.add_argument('-t', action='store_true', help='Create files (default is to read)')
    parser.add_argument('-c', action='store_true', help='Use CSV format')
    parser.add_argument('-j', action='store_true', help='Use JSON format')

    args = parser.parse_args()

    if len(args.months) != len(args.days):
        print('Wrong number of months or days ranges.')
        return 0

    create_directories(args.months, args.days, args.times, days_dictionary, times_dictionary, args.t, args.c, args.j)

    return 0


main()
