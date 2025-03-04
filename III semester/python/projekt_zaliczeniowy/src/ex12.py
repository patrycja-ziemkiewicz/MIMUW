import os
import requests
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from data_parser import DrugBankParser

def fetch_uniprot_subcell_location(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception:
        return ""

    try:
        root = ET.fromstring(resp.content)
        ns = {"up": "http://uniprot.org/uniprot"}
        for comment in root.findall("up:entry/up:comment[@type='subcellular location']", ns):
            text_el = comment.find("up:text", ns)
            if text_el is not None and text_el.text:
                return text_el.text.strip()
        return ""
    except Exception:
        return ""

def simplify_uniprot_location(desc):
    desc_lower = desc.lower()
    if "secreted" in desc_lower:
        return "Secreted"
    elif "membrane" in desc_lower:
        return "Membrane"
    elif "nucleus" in desc_lower:
        return "Nucleus"
    elif "cytoplasm" in desc_lower:
        return "Cytoplasm"
    elif "endoplasmic" in desc_lower:
        return "Endoplasmic"
    elif "lysosome" in desc_lower:
        return "Lysosome"
    elif "extracellular" in desc_lower:
        return "Extracellular"
    else:
        return "Unknown"

def enrich_targets_uniprot(df_targets):
    df_nonempty = df_targets[df_targets["uniprot_id"] != ""].copy()
    unique_ids = df_nonempty["uniprot_id"].unique()[:100]
    df_100 = df_nonempty[df_nonempty["uniprot_id"].isin(unique_ids)].copy()

    location_map = {}
    for uid in unique_ids:
        raw_loc = fetch_uniprot_subcell_location(uid) 
        simplified = simplify_uniprot_location(raw_loc)
        location_map[uid] = simplified
        
    df_100["uniprot_location"] = df_100["uniprot_id"].map(location_map)
    return df_100

def plot_two_pie_charts(df_targets, output_file):
    df_targets['cellular_location'] = df_targets['cellular_location'].fillna("Unknown")
    counts_db = df_targets['cellular_location'].value_counts()
    labels_db = counts_db.index.tolist()
    sizes_db = counts_db.values
    total_db = sizes_db.sum()
    legend_labels_db = [f"{label}: {count} ({count/total_db*100:.1f}%)" 
                        for label, count in zip(labels_db, sizes_db)]
    

    df_targets['uniprot_location'] = df_targets['uniprot_location'].fillna("Unknown")
    counts_up = df_targets['uniprot_location'].value_counts()
    labels_up = counts_up.index.tolist()
    sizes_up = counts_up.values
    total_up = sizes_up.sum()
    legend_labels_up = [f"{label}: {count} ({count/total_up*100:.1f}%)" 
                        for label, count in zip(labels_up, sizes_up)]
    
    def my_autopct(pct):
        return ('%1.1f%%' % pct) if pct >= 5 else ''
    
    fig, axes = plt.subplots(1, 2, figsize=(24, 12))
    
    wedges1, texts1, autotexts1 = axes[0].pie(sizes_db, autopct=my_autopct, startangle=140, radius=1.2)
    for autotext in autotexts1:
        autotext.set_fontsize(18)
    axes[0].set_title("DrugBank: cellular_location", fontsize=22)
    axes[0].axis('equal')
    axes[0].legend(wedges1, legend_labels_db, title="Lokalizacja", loc="lower left", 
                   bbox_to_anchor=(0, 0), fontsize=14, title_fontsize=16)

    wedges2, texts2, autotexts2 = axes[1].pie(sizes_up, autopct=my_autopct, startangle=140, radius=1.2)
    for autotext in autotexts2:
        autotext.set_fontsize(18)
    axes[1].set_title("UniProt: cellular_location", fontsize=22)
    axes[1].axis('equal')
    axes[1].legend(wedges2, legend_labels_up, title="Lokalizacja", loc="lower left", 
                   bbox_to_anchor=(0, 0), fontsize=14, title_fontsize=16)
    
    plt.tight_layout()
    plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Two pie charts saved to: {output_file}")

def task_12(xml_filename, output_folder):
    parser = DrugBankParser(xml_filename)
    df_targets = parser.parse_target_interactions()
    df_100 = enrich_targets_uniprot(df_targets)

    output = os.path.join(output_folder, "ex12_two_pies.png")
    
    plot_two_pie_charts(df_100, output)


