from data_parser import DrugBankParser
import os
    

def task_3(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    
    df_drugs = parser.parse_products()
    drugs_json_file = os.path.join(output_folder, "ex3.json")
    
    df_drugs.to_json(drugs_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Dane o lekach zapisane do: {drugs_json_file}")