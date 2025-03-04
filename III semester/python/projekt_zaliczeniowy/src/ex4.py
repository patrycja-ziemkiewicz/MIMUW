import os
from data_parser import DrugBankParser

def task_4(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    
    df_pathways = parser.parse_pathways()
    
    pathways_json_file = os.path.join(output_folder, "ex4.json")
    df_pathways.to_json(pathways_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Dane o szlakach zapisane do: {pathways_json_file}")
    
    unique_pathways = df_pathways['pathway_smpdb_id'].dropna().unique()
    total_unique = len(unique_pathways)
    print(f"Całkowita liczba unikalnych szlaków: {total_unique}")
    
    