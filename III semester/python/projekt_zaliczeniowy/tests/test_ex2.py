import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex2 import task_2


SAMPLE_XML_NORMAL = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <drug type="chemical" created="2006-01-01" updated="2024-01-02">
        <drugbank-id primary="true">DB00005</drugbank-id>
        <name>TestDrugWithSynonyms</name>
        <synonyms>
            <synonym>Synonym A</synonym>
            <synonym>Synonym B</synonym>
        </synonyms>
    </drug>
</drugbank>
'''

SAMPLE_XML_NO_DB00005 = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <drug type="chemical" created="2006-01-01" updated="2024-01-02">
        <drugbank-id primary="true">DB00006</drugbank-id>
        <name>TestDrugNoDB00005</name>
        <synonyms>
            <synonym>Synonym C</synonym>
        </synonyms>
    </drug>
</drugbank>
'''

SAMPLE_XML_EMPTY_SYNONYMS = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <drug type="chemical" created="2006-01-01" updated="2024-01-02">
        <drugbank-id primary="true">DB00005</drugbank-id>
        <name>TestDrugEmptySynonyms</name>
        <synonyms>
        </synonyms>
    </drug>
</drugbank>
'''

def test_task_2_normal(tmp_path, capsys):
    xml_file = tmp_path / "sample_normal.xml"
    xml_file.write_text(SAMPLE_XML_NORMAL, encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    task_2(str(xml_file), str(output_dir))

    json_file = output_dir / "ex2.json"
    assert json_file.exists()
    
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    expected = [
        {
            "drug_id": "DB00005",
            "synonyms": ["Synonym A", "Synonym B"]
        }
    ]
    assert data == expected

    graph_file = output_dir / "ex2_synonyms_graph.png"
    assert graph_file.exists()

    captured = capsys.readouterr().out
    assert "Dane o synonimach zapisane do:" in captured
    assert "Graf zapisany do:" in captured

def test_task_2_no_db00005(tmp_path, capsys):
    xml_file = tmp_path / "sample_no_db00005.xml"
    xml_file.write_text(SAMPLE_XML_NO_DB00005, encoding="utf-8")
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    task_2(str(xml_file), str(output_dir))

    json_file = output_dir / "ex2.json"
    assert json_file.exists()
    
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    expected = [
        {
            "drug_id": "DB00006",
            "synonyms": ["Synonym C"]
        }
    ]
    assert data == expected

    graph_file = output_dir / "ex2_synonyms_graph.png"
    assert not graph_file.exists()
    
    captured = capsys.readouterr().out
    assert "Nie znaleziono leku o DrugBank ID: DB00005" in captured

def test_task_2_empty_synonyms(tmp_path, capsys):

    xml_file = tmp_path / "sample_empty_synonyms.xml"
    xml_file.write_text(SAMPLE_XML_EMPTY_SYNONYMS, encoding="utf-8")
    
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    
    task_2(str(xml_file), str(output_dir))

    json_file = output_dir / "ex2.json"
    assert json_file.exists()
    
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    
    expected = [
        {
            "drug_id": "DB00005",
            "synonyms": []
        }
    ]
    assert data == expected

    graph_file = output_dir / "ex2_synonyms_graph.png"
    assert not graph_file.exists()
    
    captured = capsys.readouterr().out
    assert "Dla leku DB00005 nie znaleziono synonimów." in captured
