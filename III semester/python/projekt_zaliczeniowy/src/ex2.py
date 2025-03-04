import textwrap
import networkx as nx
import matplotlib.pyplot as plt
import os
from data_parser import DrugBankParser

def plot_synonyms_graph(drugbank_id, synonyms_df, output_file):
    
    record = synonyms_df[synonyms_df['drug_id'] == drugbank_id]
    if record.empty:
        print(f"Nie znaleziono leku o DrugBank ID: {drugbank_id}")
        return

    synonyms_list = record.iloc[0]['synonyms']
    if not synonyms_list:
        print(f"Dla leku {drugbank_id} nie znaleziono synonimów.")
        return

    G = nx.Graph()

    G.add_node(drugbank_id, label=drugbank_id, color='lightblue', size=800)

    for syn in synonyms_list:
        syn_str = str(syn)
        wrapped_syn = "\n".join(textwrap.wrap(syn_str, width=14))
        G.add_node(syn_str, label=wrapped_syn, color='lightgreen', size=500)
        G.add_edge(drugbank_id, syn_str)

    pos = nx.spring_layout(G, k=0.5, seed=42)

    colors = [G.nodes[node]['color'] for node in G.nodes()]
    sizes = [G.nodes[node]['size'] for node in G.nodes()]

    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=sizes)
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7)

    labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10)

    plt.title(f"Graf synonimów dla leku {drugbank_id}", fontsize=14)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()   
    print(f"Graf zapisany do: {output_file}")

def task_2(xml_filename, output_folder):
    
    parser = DrugBankParser(xml_filename)
    df_synonyms = parser.parse_synonyms()
    
    synonyms_json_file = os.path.join(output_folder, "ex2.json")
    df_synonyms.to_json(synonyms_json_file, orient='records', force_ascii=False, indent=4)
    print(f"Dane o synonimach zapisane do: {synonyms_json_file}")

    graph_output_file = os.path.join(output_folder, "ex2_synonyms_graph.png")
    plot_synonyms_graph('DB00005', df_synonyms, output_file=graph_output_file)