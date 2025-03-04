import os
from data_parser import DrugBankParser

def task_7(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    
    df_targets = parser.parse_targets()
    
    targets_json_file = os.path.join(output_folder, "ex7.json")
    df_targets.to_json(targets_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Dane o targetach zapisane do: {targets_json_file}")