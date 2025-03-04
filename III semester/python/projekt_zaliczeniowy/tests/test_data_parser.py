# tests/test_parser.py

import sys
import pytest
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from data_parser import DrugBankParser
import pandas as pd

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

@pytest.fixture
def sample_xml_file(tmp_path: Path) -> Path:
    file = tmp_path / "sample.xml"
    file.write_text(SAMPLE_XML, encoding="utf-8")
    return file

def test_parse_drugs(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_drugs()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    row = df[df['drug_id'] == "DB00001"].iloc[0]
    assert row['name'] == "Lepirudin"
    assert "recombinant hirudin" in row['description'].lower()
    assert row['state'] == "solid"
    assert 'food_interactions' in row

def test_parse_synonyms(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_synonyms()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    row = df.iloc[0]
    assert row['drug_id'] == "DB00001"
    synonyms = row['synonyms']
    assert "Lepirudin" in synonyms
    assert "Hirudin variant-1" in synonyms

def test_parse_products(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_products()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    row = df.iloc[0]
    assert row['drug_id'] == "DB00001"
    assert row['product_name'] == "Refludan"
    assert row['manufacturer'] == "Bayer"
    assert row['ndc'] == "50419-150"
    assert row['dosage_form'] == "Powder"
    assert row['route'] == "Intravenous"
    assert row['dosage'] == "50 mg/1mL"
    assert row['country'] == "US"
    assert row['regulatory_agency'] == "FDA NDC"

def test_parse_pathways(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_pathways()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    row = df.iloc[0]
    assert row['pathway_smpdb_id'] == "SMP00001"
    assert row['pathway_name'] == "Lepirudin Action Pathway"
    assert "DB00001" in row['drug_ids']

def test_parse_targets(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_targets()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    row = df.iloc[0]
    assert row['target_drugbank_id'] == "TARGET001"
    assert row['polypeptide_name'] == "Protein A"
    assert row['gene_name'] == "GENEA"
    assert row['cellular_location'] == "Nucleus"
    assert row['genatlas_id'] == "GA0001"

def test_parse_drug_status(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_drug_status()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    row = df[df['id'] == "DB00001"].iloc[0]
    assert row['name'] == "Lepirudin"
    assert "approved" in row['groups']
    assert "withdrawn" in row['groups']

def test_parse_interactions(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_interactions()
    assert df.empty

def test_parse_target_interactions(sample_xml_file):
    parser = DrugBankParser(str(sample_xml_file))
    df = parser.parse_target_interactions()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    row = df.iloc[0]
    assert row['drug_id'] == "DB00002"
    assert row['target_drugbank_id'] == "TARGET001"
    assert row['gene_name'] == "GENEA"
    assert row['uniprot_id'] == ""
