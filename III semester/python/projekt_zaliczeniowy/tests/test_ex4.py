import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex4 import task_4

SAMPLE_XML_PATHWAYS = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <pathway>
        <smpdb-id>SMP00001</smpdb-id>
        <name>Pathway One</name>
        <category>cat1</category>
        <drugs>
            <drug>
                <drugbank-id>DB00001</drugbank-id>
            </drug>
            <drug>
                <drugbank-id>DB00002</drugbank-id>
            </drug>
        </drugs>
    </pathway>
    <pathway>
        <smpdb-id>SMP00002</smpdb-id>
        <name>Pathway Two</name>
        <category>cat2</category>
        <drugs>
            <drug>
                <drugbank-id>DB00003</drugbank-id>
            </drug>
        </drugs>
    </pathway>
    <pathway>
        <smpdb-id>SMP00001</smpdb-id>
        <name>Pathway One Duplicate</name>
        <category>cat1</category>
        <drugs>
            <drug>
                <drugbank-id>DB00004</drugbank-id>
            </drug>
        </drugs>
    </pathway>
</drugbank>
'''

def test_task_4(tmp_path, capsys):
    xml_file = tmp_path / "sample_pathways.xml"
    xml_file.write_text(SAMPLE_XML_PATHWAYS, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_4(str(xml_file), str(output_dir))
    json_file = output_dir / "ex4.json"
    assert json_file.exists()
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    expected = [
        {
            "pathway_smpdb_id": "SMP00001",
            "pathway_name": "Pathway One",
            "pathway_category": "cat1",
            "drug_ids": ["DB00001", "DB00002"]
        },
        {
            "pathway_smpdb_id": "SMP00002",
            "pathway_name": "Pathway Two",
            "pathway_category": "cat2",
            "drug_ids": ["DB00003"]
        },
        {
            "pathway_smpdb_id": "SMP00001",
            "pathway_name": "Pathway One Duplicate",
            "pathway_category": "cat1",
            "drug_ids": ["DB00004"]
        }
    ]
    data_sorted = sorted(data, key=lambda x: (x["pathway_smpdb_id"], x["pathway_name"]))
    expected_sorted = sorted(expected, key=lambda x: (x["pathway_smpdb_id"], x["pathway_name"]))
    assert data_sorted == expected_sorted
    captured = capsys.readouterr().out
    assert "Dane o szlakach zapisane do:" in captured
    assert "Całkowita liczba unikalnych szlaków: 2" in captured
