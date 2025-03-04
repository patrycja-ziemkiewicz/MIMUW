import os
import random
import xml.etree.ElementTree as ET
from ex1 import task_1
from ex2 import task_2
from ex3 import task_3
from ex4 import task_4
from ex5 import task_5
from ex6 import task_6
from ex7 import task_7
from ex8 import task_8
from ex9 import task_9
from ex10 import task_10
from ex11 import task_11
from ex12 import task_12

def generate_test_database(original_xml, output_xml, n_generated):

    try:
        tree = ET.parse(original_xml)
    except Exception as e:
        print(f"Błąd wczytywania pliku {original_xml}: {e}")
        return
    root = tree.getroot()
    
    ns = {"db": "http://www.drugbank.ca"}

    base_drugs = root.findall("db:drug", ns)
    original_count = len(base_drugs)
    print("Oryginalna liczba leków:", original_count)
    if original_count == 0:
        print("Nie znaleziono leków w oryginalnej bazie!")
        return

    max_id = 0
    for drug in base_drugs:
        primary_id_elem = drug.find("db:drugbank-id[@primary='true']", ns)
        if primary_id_elem is not None and primary_id_elem.text:
            try:

                num = int(primary_id_elem.text.strip()[2:])
                if num > max_id:
                    max_id = num
            except Exception:
                pass
    new_start = max_id + 1

    for i in range(n_generated):
        template = random.choice(base_drugs)
        new_drug = ET.fromstring(ET.tostring(template, encoding="utf-8"))
        new_id = "DB" + str(new_start + i).zfill(5)
        
        primary_id_elem = new_drug.find("db:drugbank-id[@primary='true']", ns)
        if primary_id_elem is not None:
            primary_id_elem.text = new_id
        else:
            new_id_elem = ET.Element("drugbank-id", attrib={"primary": "true"})
            new_id_elem.text = new_id
            new_drug.insert(0, new_id_elem)
        
        root.append(new_drug)
    
    total_drugs = original_count + n_generated
    print(f"Łącznie leków po generacji: {total_drugs}")

    tree.write(output_xml, encoding="utf-8", xml_declaration=True)
    print(f"Testowa baza danych zapisana do: {output_xml}")

def task_13(xml_filename, output_folder, n_generated, perform_tasks):
    output_xml = "drugbank_partial_and_generated.xml"
    
    generate_test_database(xml_filename, output_xml, n_generated)
    
    ex3_folder = os.path.join(output_folder, "ex13")
    os.makedirs(ex3_folder, exist_ok=True)
    
    if perform_tasks:
        task_1(output_xml, ex3_folder)
        task_2(output_xml, ex3_folder)
        task_3(output_xml, ex3_folder)
        task_4(output_xml, ex3_folder)
        task_5(output_xml, ex3_folder)
        task_6(output_xml, ex3_folder)
        task_7(output_xml, ex3_folder)
        task_8(output_xml, ex3_folder)
        task_9(output_xml, ex3_folder)
        task_10(output_xml, ex3_folder)
        task_11(output_xml, ex3_folder)
        task_12(output_xml, ex3_folder)

