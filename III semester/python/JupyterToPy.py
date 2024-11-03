import json
import argparse
import os
import re

def load_file(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"Plik '{file_name}' nie został znaleziony.")
    except json.JSONDecodeError:
        print("Błąd odczytu pliku. Upewnij się, że jest to prawidłowy plik .ipynb.")

def text_formatting(text, divider, max_length = 79):
    words = re.split(r'(\s+)', text) 
    lines = []         
    current_line = "" 
    for word in words:
        if (len(current_line) + len(word) > max_length):
            lines.append(current_line)
            current_line = word    
        else:
            current_line += word

    if current_line:
        lines.append(current_line)
    return divider.join(lines)

def process_data(data):
    if data.get("cell_type") == 'markdown':
        wrapped_lines = ""
        for line in data.get("source"):
            wrapped_lines += '# ' + text_formatting(line, '\n# ')
        return wrapped_lines
    else:
        return "".join(data.get("source"))

def write_data(output_file_name, processed_data):
    with open(output_file_name, "w", encoding="utf-8") as file:
        for line in processed_data:
            file.write("\n" + line + "\n")

def count_exercises(cells):
    exercises = filter(lambda cell: cell.get("cell_type") == "markdown" 
                       and "# Ćwiczenie" in cell["source"][0], cells)
    
    return sum(1 for _ in exercises)

def main():
    parser = argparse.ArgumentParser(description="Program do wczytywania pliku .ipynb")
    parser.add_argument("file_name", help="Ścieżka do pliku .ipynb")
    args = parser.parse_args()

    data = load_file(args.file_name)

    base_name, _ = os.path.splitext(args.file_name)  
    output_file_name = base_name + ".py" 

    processed_data = list(map(process_data, data.get("cells")))
    write_data(output_file_name, processed_data)

    print(count_exercises(data.get("cells")))

    

main()
