import os
import matplotlib.pyplot as plt
from data_parser import DrugBankParser

def plot_cellular_location_pie_chart(df_targets, output_file):

    df_targets['cellular_location'] = df_targets['cellular_location'].fillna("Unknown")
    
    counts = df_targets['cellular_location'].value_counts()
    labels = counts.index.tolist()
    sizes = counts.values
    total = sum(sizes)
    
    legend_labels = [f"{label}: {count} ({count/total*100:.1f}%)" 
                     for label, count in zip(labels, sizes)]
    
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct >= 5 else ''
    
    plt.figure(figsize=(12, 12))

    wedges, texts, autotexts = plt.pie(sizes, autopct=my_autopct, startangle=140, radius=1.2)
    
    for autotext in autotexts:
        autotext.set_fontsize(16)
    
    plt.title("Procentowe występowanie targetów w różnych częściach komórki", fontsize=16)
    plt.axis('equal')
    
    plt.legend(wedges, legend_labels, title="Lokalizacja", loc="lower left", 
               bbox_to_anchor=(0, 0), fontsize=12, title_fontsize=14)
    
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Pie chart saved to: {output_file}")

def task_8(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    df_targets = parser.parse_targets()
    output_file = os.path.join(output_folder, "ex8_targets_cellular_location_pie_chart.png")

    plot_cellular_location_pie_chart(df_targets, output_file)