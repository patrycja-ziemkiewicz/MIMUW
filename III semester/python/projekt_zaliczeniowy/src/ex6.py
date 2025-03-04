import os
import matplotlib.pyplot as plt
import pandas as pd
from data_parser import DrugBankParser

def create_drug_pathway_counts(df_pathways):
    
    drug_counts = {}
    for idx, row in df_pathways.iterrows():
        for drug in row['drug_ids']:
            drug_counts[drug] = drug_counts.get(drug, 0) + 1
    return drug_counts

def plot_drug_pathway_histogram(drug_counts, output_file):

    sorted_items = sorted(drug_counts.items(), key=lambda x: x[0])
    drugs = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]
    
    plt.figure(figsize=(12, 6))
    plt.bar(drugs, counts, color='skyblue', edgecolor='black')
    plt.xlabel("DrugBank ID (lek)")
    plt.ylabel("Liczba szlaków")
    plt.title("Liczba szlaków dla poszczególnych leków")
    plt.xticks(rotation=90)  
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()
    print(f"Bar chart saved to: {output_file}")

def task_6(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    
    df_pathways = parser.parse_pathways()
    
    drug_counts = create_drug_pathway_counts(df_pathways)
    
    df_drug_counts = pd.DataFrame([
        {"drug_id": drug, "pathway_count": count} 
        for drug, count in drug_counts.items()
    ])
    
    drug_counts_json = os.path.join(output_folder, "ex6.json")
    df_drug_counts.to_json(drug_counts_json, orient='records', force_ascii=False, indent=4)
    print(f"Dane o liczbie szlaków dla leków zapisane do: {drug_counts_json}")
    
    histogram_file = os.path.join(output_folder, "ex6_drug_pathway_histogram.png")
    plot_drug_pathway_histogram(drug_counts, histogram_file)