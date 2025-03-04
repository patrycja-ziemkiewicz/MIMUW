from data_parser import DrugBankParser
import os
from pathlib import Path
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
from ex13 import task_13

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    output_folder = os.path.join(base_dir, "output")
    xml_file = "drugbank_partial.xml"
    
    task_1(xml_file, output_folder)
    task_1(xml_file, output_folder)
    task_2(xml_file, output_folder)
    task_3(xml_file, output_folder)
    task_4(xml_file, output_folder)
    task_5(xml_file, output_folder)
    task_6(xml_file, output_folder)
    task_7(xml_file, output_folder)
    task_8(xml_file, output_folder)
    task_9(xml_file, output_folder)
    task_10(xml_file, output_folder)
    task_11(xml_file, output_folder)
    task_12(xml_file, output_folder)
    task_13(xml_file, output_folder, 100, False)