import networkx as nx
import matplotlib.pyplot as plt
import os
from data_parser import DrugBankParser

def plot_bipartite_pathways_drugs(df_pathways, output_file):
    B = nx.Graph()

    pathway_nodes = []
    drug_nodes = set()
    
    for idx, row in df_pathways.iterrows():
        
        p_node = row['pathway_smpdb_id']
        p_label = row['pathway_name'] if row['pathway_name'] is not None else p_node
        B.add_node(p_node, bipartite=0, label=p_label)
        pathway_nodes.append(p_node)
        
        for drug in row['drug_ids']:
            drug_nodes.add(drug)
            B.add_node(drug, bipartite=1, label=drug)
            B.add_edge(p_node, drug)
    
    pos = nx.bipartite_layout(B, pathway_nodes)
    
    plt.figure(figsize=(12, 8))
    
    nx.draw_networkx_nodes(B, pos, nodelist=pathway_nodes, node_color='lightblue', node_size=800, label='Szlaki')
    nx.draw_networkx_nodes(B, pos, nodelist=list(drug_nodes), node_color='lightgreen', node_size=500, label='Leki')
    
    nx.draw_networkx_edges(B, pos, alpha=0.7)

    labels = nx.get_node_attributes(B, 'label')
    nx.draw_networkx_labels(B, pos, labels, font_size=10)
    
    plt.title("Graf dwudzielny: Szlaki i leki")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300)
    plt.close()
    print(f"Bipartite graph saved to: {output_file}")

def task_5(xml_filename, output_folder):

    parser = DrugBankParser(xml_filename)
    
    df_pathways = parser.parse_pathways()
    
    output_file = os.path.join(output_folder, "ex5_bipartite_graph.png")
    
    plot_bipartite_pathways_drugs(df_pathways, output_file)