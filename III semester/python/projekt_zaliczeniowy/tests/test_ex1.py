import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex1 import task_1

SAMPLE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
    <drug type="biotech" created="2005-06-13" updated="2024-01-02">
        <drugbank-id primary="true">DB00001</drugbank-id>
        <drugbank-id>BTD00024</drugbank-id>
        <name>Lepirudin</name>
        <description>Lepirudin is a recombinant hirudin.</description>
        <state>solid</state>
        <groups>
            <group>approved</group>
            <group>withdrawn</group>
        </groups>
        <products>
            <product>
                <name>Refludan</name>
                <labeller>Bayer</labeller>
                <ndc-product-code>50419-150</ndc-product-code>
                <dosage-form>Powder</dosage-form>
                <route>Intravenous</route>
                <strength>50 mg/1mL</strength>
                <country>US</country>
                <source>FDA NDC</source>
            </product>
        </products>
        <synonyms>
            <synonym>Lepirudin</synonym>
            <synonym>Hirudin variant-1</synonym>
        </synonyms>
    </drug>
    <drug type="chemical" created="2006-01-01" updated="2024-01-02">
        <drugbank-id primary="true">DB00002</drugbank-id>
        <name>TestDrug</name>
        <targets>
            <target>
                <id>TARGET001</id>
                <polypeptide id="P00001" source="UniProtKB">
                    <name>Protein A</name>
                    <gene-name>GENEA</gene-name>
                    <cellular-location>Nucleus</cellular-location>
                    <external-identifiers>
                        <external-identifier>
                            <resource>GenAtlas</resource>
                            <identifier>GA0001</identifier>
                        </external-identifier>
                    </external-identifiers>
                </polypeptide>
            </target>
        </targets>
    </drug>
    <pathway>
        <smpdb-id>SMP00001</smpdb-id>
        <name>Lepirudin Action Pathway</name>
        <category>drug_action</category>
        <drugs>
            <drug>
                <drugbank-id>DB00001</drugbank-id>
            </drug>
        </drugs>
    </pathway>
</drugbank>
"""

def test_task_1_correct_output(tmp_path, capsys):

    xml_file = tmp_path / "sample.xml"
    xml_file.write_text(SAMPLE_XML, encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    task_1(str(xml_file), str(output_dir))

    json_file = output_dir / "ex1.json"
    assert json_file.exists()

    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
        
    expected = [
        {
            "drug_id": "DB00001",
            "name": "Lepirudin",
            "type": "biotech",
            "description": "Lepirudin is a recombinant hirudin.",
            "state": "solid",
            "indication": None,
            "mechanism_of_action": None,
            "food_interactions": None
        },
        {
            "drug_id": "DB00002",
            "name": "TestDrug",
            "type": "chemical",
            "description": None,
            "state": None,
            "indication": None,
            "mechanism_of_action": None,
            "food_interactions": None
        }
    ]

    assert data == expected

    # Sprawdź komunikat wypisywany przez task_1
    captured = capsys.readouterr().out.strip()
    expected_message = f"Dane o lekach zapisane do: {json_file}"
    assert expected_message in captured

def test_task_1_no_drug_elements(tmp_path):

    no_drug_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <drugbank xmlns="http://www.drugbank.ca">
        <pathway>
            <smpdb-id>SMP00001</smpdb-id>
            <name>Pathway Test</name>
        </pathway>
    </drugbank>
    """
    xml_file = tmp_path / "nodrugs.xml"
    xml_file.write_text(no_drug_xml, encoding="utf-8")

    output_dir = tmp_path / "output"
    output_dir.mkdir()

    task_1(str(xml_file), str(output_dir))

    json_file = output_dir / "ex1.json"
    assert json_file.exists()

    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert data == []

