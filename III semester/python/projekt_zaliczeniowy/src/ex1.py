from data_parser import DrugBankParser
import os
from pathlib import Path

def task_1(xml_filename, output_folder):
    
    parser = DrugBankParser(xml_filename)
    
    df_drugs = parser.parse_drugs()
    drugs_json_file = os.path.join(output_folder, "ex1.json")
    
    df_drugs.to_json(drugs_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Dane o lekach zapisane do: {drugs_json_file}")
    
    

    
    
    
    