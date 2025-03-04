import xml.etree.ElementTree as ET
import pandas as pd

class DrugBankParser:
    
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.ns = {'db': 'http://www.drugbank.ca'}

    def parse_drugs(self):
        
        context = ET.iterparse(self.xml_file, events=('end',))
        data = []
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                drug_data = {}
                unique_id = elem.find('db:drugbank-id[@primary="true"]', self.ns)

                drug_data['drug_id'] = unique_id.text.strip() if unique_id is not None and unique_id.text else None
                
                if (drug_data['drug_id'] == None):
                    elem.clear()
                    continue

                name_elem = elem.find('db:name', self.ns)
                drug_data['name'] = name_elem.text.strip() if name_elem is not None and name_elem.text else None

                drug_data['type'] = elem.attrib.get('type', 'None').strip()

                desc_elem = elem.find('db:description', self.ns)
                drug_data['description'] = desc_elem.text.strip() if desc_elem is not None and desc_elem.text else None

                state_elem = elem.find('db:state', self.ns)
                drug_data['state'] = state_elem.text.strip() if state_elem is not None and state_elem.text else None

                indication_elem = elem.find('db:indication', self.ns)
                drug_data['indication'] = indication_elem.text.strip() if indication_elem is not None and indication_elem.text else None

                moa_elem = elem.find('db:mechanism-of-action', self.ns)
                drug_data['mechanism_of_action'] = moa_elem.text.strip() if moa_elem is not None and moa_elem.text else None

                food_int_elem = elem.find('db:food-interactions', self.ns)
                if food_int_elem is not None:
                    interactions = [fi.text.strip() for fi in food_int_elem.findall('db:food-interaction', self.ns) if fi.text]
                    drug_data['food_interactions'] = '; '.join(interactions) if interactions else None
                else:
                    drug_data['food_interactions'] = None

                data.append(drug_data)
                
                elem.clear()

              
        df_drugs = pd.DataFrame(data)      
        return df_drugs
    
    def parse_synonyms(self):
        
        context = ET.iterparse(self.xml_file, events=('end',))
        data = []
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                drug_data = {}
                unique_id = elem.find('db:drugbank-id[@primary="true"]', self.ns)
                
                drug_data['drug_id'] = unique_id.text.strip() if unique_id is not None and unique_id.text else None
                
                if (drug_data['drug_id'] == None):
                    elem.clear()
                    continue

                synonyms_list = []
                synonyms_elem = elem.find('db:synonyms', self.ns)
                if synonyms_elem is not None:
                    for syn in synonyms_elem.findall('db:synonym', self.ns):
                        if syn.text:
                            synonyms_list.append(syn.text.strip())
                drug_data['synonyms'] = synonyms_list

                data.append(drug_data)
                elem.clear()
             
        df_drugs = pd.DataFrame(data)      
        return df_drugs
    
    def parse_products(self):
        
        context = ET.iterparse(self.xml_file, events=('end',))
        data = []
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                unique_id = elem.find('db:drugbank-id[@primary="true"]', self.ns)
                drug_id = unique_id.text.strip() if unique_id is not None and unique_id.text else None
                if drug_id is None:
                    elem.clear()
                    continue

                products = elem.find('db:products', self.ns)
                if products is not None:
                    for product in products.findall('db:product', self.ns):
                        record = {}
                        record['drug_id'] = drug_id

                        prod_name = product.find('db:name', self.ns)
                        record['product_name'] = prod_name.text.strip() if prod_name is not None and prod_name.text else None

                        manufacturer = product.find('db:labeller', self.ns)
                        record['manufacturer'] = manufacturer.text.strip() if manufacturer is not None and manufacturer.text else None

                        ndc = product.find('db:ndc-product-code', self.ns)
                        record['ndc'] = ndc.text.strip() if ndc is not None and ndc.text else None

                        dosage_form = product.find('db:dosage-form', self.ns)
                        record['dosage_form'] = dosage_form.text.strip() if dosage_form is not None and dosage_form.text else None

                        route = product.find('db:route', self.ns)
                        record['route'] = route.text.strip() if route is not None and route.text else None

                        strength = product.find('db:strength', self.ns)
                        record['dosage'] = strength.text.strip() if strength is not None and strength.text else None

                        country = product.find('db:country', self.ns)
                        record['country'] = country.text.strip() if country is not None and country.text else None

                        
                        reg = product.find('db:source', self.ns)
                        record['regulatory_agency'] = reg.text.strip() if reg is not None and reg.text else None

                        data.append(record)
                elem.clear()
                
        df_products = pd.DataFrame(data)
        return df_products
    
    
    def parse_pathways(self):
        
        data = []
        context = ET.iterparse(self.xml_file, events=('end',))
        
        for event, elem in context:
            if elem.tag.endswith('pathway'):
                record = {}
                
                smpdb_id = elem.find('db:smpdb-id', self.ns)
                record['pathway_smpdb_id'] = smpdb_id.text.strip() if smpdb_id is not None and smpdb_id.text else None

                pathway_name = elem.find('db:name', self.ns)
                record['pathway_name'] = pathway_name.text.strip() if pathway_name is not None and pathway_name.text else None
                
                category = elem.find('db:category', self.ns)
                record['pathway_category'] = category.text.strip() if category is not None and category.text else None

                drugs = elem.find('db:drugs', self.ns)
                drug_ids = []
                
                if drugs is not None:
                    for d in drugs.findall('db:drug', self.ns):
                        id_el = d.find('db:drugbank-id', self.ns)
                        if id_el is not None and id_el.text:
                            drug_ids.append(id_el.text.strip())
                record['drug_ids'] = drug_ids
                data.append(record)

        df_pathways = pd.DataFrame(data)
        return df_pathways
    
    def parse_targets(self):

        data = []
        context = ET.iterparse(self.xml_file, events=('end',))
        for event, elem in context:
            if elem.tag.endswith('target'):
                record = {}
                
                target_id = elem.find('db:id', self.ns)
                record['target_drugbank_id'] = target_id.text.strip() if target_id is not None and target_id.text else None

                poly = elem.find('db:polypeptide', self.ns)
                if poly is not None:
                    record['source'] = poly.attrib.get('source', None)
                    
                    ext_id = poly.attrib.get('id').strip()
                    
                    record['external_id'] = ext_id

                    poly_name = poly.find('db:name', self.ns)
                    record['polypeptide_name'] = poly_name.text.strip() if poly_name is not None and poly_name.text else None

                    gene = poly.find('db:gene-name', self.ns)
                    record['gene_name'] = gene.text.strip() if gene is not None and gene.text else None

                    genatlas_id = None
                    ext_ids = poly.find('db:external-identifiers', self.ns)
                    if ext_ids is not None:
                        for ext in ext_ids.findall('db:external-identifier', self.ns):
                            res = ext.find('db:resource', self.ns)
                            ident = ext.find('db:identifier', self.ns)
                            if res is not None and ident is not None:
                                if res.text.strip() == "GenAtlas":
                                    genatlas_id = ident.text.strip()
                                    break
                    record['genatlas_id'] = genatlas_id

                    chrom = poly.find('db:chromosome-location', self.ns)
                    record['chromosome'] = chrom.text.strip() if chrom is not None and chrom.text else None

                    cell = poly.find('db:cellular-location', self.ns)
                    record['cellular_location'] = cell.text.strip() if cell is not None and cell.text else None
                

                data.append(record)
                elem.clear()
                
        df_target = pd.DataFrame(data)
        return df_target
    
    
    def parse_drug_status(self):
        data = []
        context = ET.iterparse(self.xml_file, events=('end',))
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                drug_data = {}
                unique_id = elem.find('db:drugbank-id[@primary="true"]', self.ns)
                drug_data['id'] = unique_id.text.strip() if unique_id is not None and unique_id.text else None
                if drug_data['id'] is None:
                    elem.clear()
                    continue

                name_elem = elem.find('db:name', self.ns)
                drug_data['name'] = name_elem.text.strip() if name_elem is not None and name_elem.text else None

                groups_elem = elem.find('db:groups', self.ns)
                if groups_elem is not None:
                    groups = [g.text.strip().lower() for g in groups_elem.findall('db:group', self.ns) if g.text]
                else:
                    groups = []
                drug_data['groups'] = groups

                data.append(drug_data)
                elem.clear()
        df_status = pd.DataFrame(data)
        return df_status
    
    def parse_interactions(self):
    
        data = []
        context = ET.iterparse(self.xml_file, events=('end',))
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                main_id_elem = elem.find('db:drugbank-id[@primary="true"]', self.ns)
                main_id = main_id_elem.text.strip() if main_id_elem is not None and main_id_elem.text else None
                if main_id is None:
                    elem.clear()
                    continue

                interactions = elem.find('db:drug-interactions', self.ns)
                if interactions is not None:
                    for inter in interactions.findall('db:drug-interaction', self.ns):
                        record = {}
                        record['drug_id'] = main_id
                        inter_id_elem = inter.find('db:drugbank-id', self.ns)
                        record['interacting_drugbank_id'] = (inter_id_elem.text.strip()
                                                            if inter_id_elem is not None and inter_id_elem.text
                                                            else None)
                        inter_name_elem = inter.find('db:name', self.ns)
                        record['interacting_drug_name'] = (inter_name_elem.text.strip()
                                                        if inter_name_elem is not None and inter_name_elem.text
                                                        else None)
                        inter_desc_elem = inter.find('db:description', self.ns)
                        record['interaction_description'] = (inter_desc_elem.text.strip()
                                                            if inter_desc_elem is not None and inter_desc_elem.text
                                                            else None)
                        data.append(record)
                elem.clear()
        df_interactions = pd.DataFrame(data)
        return df_interactions
    
    
    def parse_target_interactions(self):

        data = []
        context = ET.iterparse(self.xml_file, events=('end',))
        
        for event, elem in context:
            if elem.tag.endswith('drug'):
                drug_id_elem = elem.find('db:drugbank-id[@primary="true"]', self.ns)
                drug_id = drug_id_elem.text.strip() if drug_id_elem is not None and drug_id_elem.text else None
                if drug_id is None:
                    elem.clear()
                    continue

                targets = elem.find('db:targets', self.ns)
                if targets is not None:
                    for targ in targets.findall('db:target', self.ns):
                        record = {}
                        record['drug_id'] = drug_id

                        target_id_elem = targ.find('db:id', self.ns)
                        record['target_drugbank_id'] = (target_id_elem.text.strip()
                                                        if target_id_elem is not None and target_id_elem.text
                                                        else None)
                        
                        poly = targ.find('db:polypeptide', self.ns)
                        if poly is not None: 
                            poly_name = poly.find('db:name', self.ns)
                            record['polypeptide_name'] = (poly_name.text.strip()
                                                        if poly_name is not None and poly_name.text
                                                        else None)
                            
                            gene = poly.find('db:gene-name', self.ns)
                            record['gene_name'] = (gene.text.strip()
                                                if gene is not None and gene.text
                                                else None)
                            
                            cell = poly.find('db:cellular-location', self.ns)
                            record['cellular_location'] = cell.text.strip() if cell is not None and cell.text else None
                            
                            uniprot_id = ""
                            ext_ids = poly.find('db:external-identifiers', self.ns)
                            if ext_ids is not None:
                                for ext in ext_ids.findall('db:external-identifier', self.ns):
                                    res = ext.find('db:resource', self.ns)
                                    ident = ext.find('db:identifier', self.ns)
                                    if res is not None and ident is not None:
                                        if res.text.strip() == "UniProtKB":
                                            uniprot_id = ident.text.strip()
                                            break
                            record['uniprot_id'] = uniprot_id
                            data.append(record)
                elem.clear()
        df_target_interactions = pd.DataFrame(data)
        return df_target_interactions
    
    
    
    
    
    
