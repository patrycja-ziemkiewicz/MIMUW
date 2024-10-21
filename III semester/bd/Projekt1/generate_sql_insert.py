import csv


input_file = 'Publikacje.csv'  
output_file = 'insert_publications.sql'

with open(input_file, 'r', encoding='utf-8') as csvfile, open(output_file, 'w', encoding='utf-8') as sqlfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        id = row['ID']
        title = row['TytuĹ‚'].replace("'", "''")  # Escaping pojedynczych cudzyslow
        year = row['Rok']
        authors = row['Autorzy']
        points = row['Punkty']
        insert = f"INSERT INTO PUBLICATIONS (id, tytul, rok, autorzy, punkty) VALUES ({id}, '{title}', {year}, {authors}, {points});\n"
        sqlfile.write(insert)

print(f'Polecenia INSERT zostaĹ‚y zapisane w pliku {output_file}')
