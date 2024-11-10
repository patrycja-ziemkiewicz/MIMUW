import csv
import os

# pliki csv
input_files = {
    "prace": "Prace.csv",
    "autorzy": "Autorzy.csv",
    "autorstwo": "Autorstwo.csv"
}


def generate_insert_statements(input_file, table_name, columns):
    insert_statements = []
    with open(input_file, mode='r', encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            values = []
            for column in columns:
                value = row[column]
                if value.isdigit():
                    values.append(value)  
                else:
                    text_value = value.replace("'", "''")
                    values.append(f"'{text_value}'") 
            insert_statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
            insert_statements.append(insert_statement)
    return insert_statements


tables = {
    "prace": ["id", "tytul", "rok", "autorzy", "punkty"],
    "autorzy": ["id", "ryzyko", "sloty"],
    "autorstwo": ["praca", "autor"]
}


with open("plik_do_zaladowania.sql", mode='w', encoding='utf-8') as sql_file:
    for table_name, columns in tables.items():
        input_file = input_files[table_name]
        insert_statements = generate_insert_statements(input_file, table_name, columns)
        for statement in insert_statements:
            sql_file.write(statement + "\n")

print("Dodane inserty")