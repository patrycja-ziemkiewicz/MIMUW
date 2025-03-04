from data_parser import DrugBankParser
import os


def task_10(xml_filename, output_folder):
    given_drug_id = "DB00002"

    parser = DrugBankParser(xml_filename)
    
    df_interactions = parser.parse_interactions()
    df_given_interactions = df_interactions[df_interactions['drug_id'] == given_drug_id]
    
    interactions_json_file = os.path.join(output_folder, "ex10.json")
    
    df_given_interactions.to_json(interactions_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Dane o interakcjach dla leku {given_drug_id} zapisane do: {interactions_json_file}")