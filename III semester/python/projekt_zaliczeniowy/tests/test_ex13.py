import os
import xml.etree.ElementTree as ET
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex13 import task_13

def test_task_13_generation(tmp_path, capsys):
    sample_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <drugbank xmlns="http://www.drugbank.ca">
    <drug type="chemical">
        <drugbank-id primary="true">DB00001</drugbank-id>
        <name>Drug One</name>
    </drug>
    <drug type="chemical">
        <drugbank-id primary="true">DB00002</drugbank-id>
        <name>Drug Two</name>
    </drug>
    </drugbank>
    '''
    original_xml = tmp_path / "original.xml"
    original_xml.write_text(sample_xml, encoding="utf-8")
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        task_13(str(original_xml), str(output_folder), 3, perform_tasks=False)
    finally:
        os.chdir(old_cwd)

    generated_xml = tmp_path / "drugbank_partial_and_generated.xml"
    assert generated_xml.exists()
    tree = ET.parse(generated_xml)
    root = tree.getroot()
    ns = {"db": "http://www.drugbank.ca"}
    drugs = root.findall("db:drug", ns)
    assert len(drugs) == 5
    captured = capsys.readouterr().out
    assert "Oryginalna liczba leków:" in captured
    assert "Łącznie leków po generacji:" in captured
    assert "Testowa baza danych zapisana do:" in captured

def test_task_13_no_drugs(tmp_path, capsys):
    sample_no_drugs = '''<?xml version="1.0" encoding="UTF-8"?>
    <drugbank xmlns="http://www.drugbank.ca">
    </drugbank>
    '''
    original_xml = tmp_path / "nodrugs.xml"
    original_xml.write_text(sample_no_drugs, encoding="utf-8")
    output_folder = tmp_path / "output"
    output_folder.mkdir()

    old_cwd = os.getcwd()
    os.chdir(tmp_path)
    try:
        task_13(str(original_xml), str(output_folder), n_generated=3, perform_tasks=False)
    finally:
        os.chdir(old_cwd)

    generated_xml = tmp_path / "drugbank_partial_and_generated.xml"
    assert not generated_xml.exists()
    captured = capsys.readouterr().out
    assert "Nie znaleziono leków w oryginalnej bazie!" in captured

def test_generate_test_database_invalid_xml(tmp_path, capsys):
    invalid_xml_file = tmp_path / "invalid.xml"
    invalid_xml_file.write_text("Not valid XML", encoding="utf-8")
    output_xml = tmp_path / "output.xml"
    task_13(str(invalid_xml_file), str(output_xml), 3, perform_tasks=False)
    captured = capsys.readouterr().out
    assert f"Błąd wczytywania pliku {invalid_xml_file}:" in captured