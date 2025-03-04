import os
import networkx as nx
import matplotlib.pyplot as plt
import imageio
import tempfile
import textwrap
import numpy as np
from data_parser import DrugBankParser

def build_gene_drug_product_graph(gene, df_target_interactions, df_drugs, df_products):

    G = nx.Graph()
    
    gene_node = f"GENE:{gene}"
    G.add_node(gene_node, group='gene', label=gene)

    df_sel_targets = df_target_interactions[
        df_target_interactions['gene_name'].str.lower() == gene.lower()
    ]
    
    drug_ids = df_sel_targets['drug_id'].dropna().unique()

    df_sel_drugs = df_drugs[df_drugs['drug_id'].isin(drug_ids)]
    
    drug_nodes = []
    for _, row in df_sel_drugs.iterrows():
        d_id = row['drug_id']
        d_label = row['name'] if row['name'] else d_id
        G.add_node(d_id, group='drug', label=d_label)
        G.add_edge(gene_node, d_id)
        drug_nodes.append(d_id)

    df_sel_products = df_products[df_products['drug_id'].isin(drug_ids)]
    for _, row in df_sel_products.iterrows():
        p_label = row['product_name'] if row['product_name'] else "Unnamed product"
        p_node = f"{row['drug_id']}::PROD::{p_label}"
        G.add_node(p_node, group='product', label=p_label)
        G.add_edge(row['drug_id'], p_node)
    
    return G, drug_nodes

def create_gene_animation(gene, G, drug_nodes, output_gif, duration=0.5):
    frames = []

    fig, ax = plt.subplots(figsize=(6,6))
    ax.text(0.5, 0.5, f"Gene: {gene}", fontsize=30, ha='center', va='center', fontweight='bold')
    ax.axis('off')
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(temp_file.name, bbox_inches='tight')
    plt.close(fig)
    frames.append(imageio.imread(temp_file.name))
    os.remove(temp_file.name)


    for d_id in drug_nodes:
        product_neighbors = [nbr for nbr in G.neighbors(d_id) if G.nodes[nbr].get('group') == 'product']

        sub_nodes = {d_id} | set(product_neighbors)
        subG = G.subgraph(sub_nodes).copy()

        fig, ax = plt.subplots(figsize=(6,6))
        pos = {}
        pos[d_id] = (0, 0)

        r = 1.2
        n_prods = len(product_neighbors)
        if n_prods > 0:
            for i, prod in enumerate(sorted(product_neighbors)):
                angle = 2 * np.pi * i / n_prods
                pos[prod] = (r * np.cos(angle), r * np.sin(angle))

        ax.scatter(*pos[d_id], s=2000, c='lightblue', edgecolors='black', zorder=2)

        drug_label = subG.nodes[d_id].get('label', d_id)
        wrapped_drug_label = "\n".join(textwrap.wrap(drug_label, width=12))
        ax.text(*pos[d_id], wrapped_drug_label, ha='center', va='center', fontsize=12, fontweight='bold', zorder=3)

        for node in subG.nodes():
            if node == d_id:
                continue
            group = subG.nodes[node].get('group')
            if group == 'product':
                ax.scatter(*pos[node], s=1200, c='lightgreen', edgecolors='black', zorder=2)
                prod_label = subG.nodes[node].get('label', node)
                wrapped_prod_label = "\n".join(textwrap.wrap(prod_label, width=12))
                ax.text(*pos[node], wrapped_prod_label, ha='center', va='center', fontsize=10, fontweight='bold', zorder=3)
                ax.plot([pos[d_id][0], pos[node][0]], [pos[d_id][1], pos[node][1]], color='gray', zorder=1)

        ax.set_title(f"Lek: {drug_label}", fontsize=14)
        margin = 0.5
        ax.set_xlim(-r-margin, r+margin)
        ax.set_ylim(-r-margin, r+margin)
        ax.axis('off')

        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp_file.name, bbox_inches='tight')
        plt.close(fig)
        frames.append(imageio.imread(temp_file.name))
        os.remove(temp_file.name)

    imageio.mimsave(output_gif, frames, duration=1)
    print(f"Animowany GIF zapisany do: {output_gif}")

def task_11(xml_filename, output_folder):
    
    parser = DrugBankParser(xml_filename)
    
    df_drugs = parser.parse_drugs()
    df_target_interactions = parser.parse_target_interactions()
    df_products = parser.parse_products()

    gene = "F2" 

    G, drug_nodes = build_gene_drug_product_graph(gene, df_target_interactions, df_drugs, df_products)
    
    output_gif = os.path.join(output_folder, f"ex11_gene_{gene}_animation.gif")
    create_gene_animation(gene, G, drug_nodes, output_gif, duration=1.5)