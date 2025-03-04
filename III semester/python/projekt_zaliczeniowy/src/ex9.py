import os
import matplotlib.pyplot as plt
import pandas as pd
from data_parser import DrugBankParser

def get_drug_status_summary(df_status):

    in_group = lambda groups, target: target in groups

    approved_count = df_status['groups'].apply(lambda gs: in_group(gs, 'approved')).sum()
    withdrawn_count = df_status['groups'].apply(lambda gs: in_group(gs, 'withdrawn')).sum()
    experimental_count = df_status['groups'].apply(lambda gs: (in_group(gs, 'experimental') or in_group(gs, 'investigational'))).sum()
    animal_count = df_status['groups'].apply(lambda gs: (in_group(gs, 'vet_approved'))).sum()
    
    approved_not_withdrawn = df_status['groups'].apply(lambda gs: (in_group(gs, 'approved') and not in_group(gs, 'withdrawn'))).sum()
    
    summary = {
        'approved': approved_count,
        'withdrawn': withdrawn_count,
        'experimental/investigational': experimental_count,
        'vet_approved': animal_count
    }
    return summary, approved_not_withdrawn

def plot_drug_status_pie_chart(summary, output_file):

    labels = list(summary.keys())
    sizes = list(summary.values())
    
    
    plt.figure(figsize=(10, 10))
    wedges, texts, autotexts = plt.pie(sizes, autopct='%1.1f%%', startangle=140)
    plt.title("Status leków", fontsize=20)
    plt.axis('equal')  
    
    for autotext in autotexts:
        autotext.set_fontsize(16)

    leg = plt.legend(wedges, labels, title="Status", loc="best", fontsize=14)
    leg.get_title().set_fontsize(15) 
    
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Pie chart saved to: {output_file}")

def task_9(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    
    df_status = parser.parse_drug_status()

    summary, approved_not_withdrawn = get_drug_status_summary(df_status)

    summary_json_file = os.path.join(output_folder, "ex9.json")
    summary_list = [{"Status": key, "Count": value} for key, value in summary.items()]
    df_summary = pd.DataFrame(summary_list)
    df_summary.to_json(summary_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Status summary saved to: {summary_json_file}")

    pie_chart_file = os.path.join(output_folder, "ex9_drug_status_pie_chart.png")
    plot_drug_status_pie_chart(summary, pie_chart_file)
    
    print("Liczba zatwierdzonych leków, które nie zostały wycofane:", approved_not_withdrawn)