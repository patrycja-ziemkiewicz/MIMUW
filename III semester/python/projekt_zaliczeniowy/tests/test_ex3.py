import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex3 import task_3


SAMPLE_XML_PRODUCTS = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB12345</drugbank-id>
    <name>SampleDrug</name>
    <products>
      <product>
         <name>Product A</name>
         <labeller>Manufacturer A</labeller>
         <ndc-product-code>12345</ndc-product-code>
         <dosage-form>Tablet</dosage-form>
         <route>Oral</route>
         <strength>10 mg</strength>
         <country>USA</country>
         <source>FDA</source>
      </product>
      <product>
         <name>Product B</name>
         <labeller>Manufacturer B</labeller>
         <ndc-product-code>67890</ndc-product-code>
         <dosage-form>Capsule</dosage-form>
         <route>Oral</route>
         <strength>20 mg</strength>
         <country>Canada</country>
         <source>Health Canada</source>
      </product>
    </products>
  </drug>
</drugbank>
'''

def test_task_3_normal(tmp_path, capsys):
    xml_file = tmp_path / "sample_products.xml"
    xml_file.write_text(SAMPLE_XML_PRODUCTS, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_3(str(xml_file), str(output_dir))
    json_file = output_dir / "ex3.json"
    assert json_file.exists()
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    expected = [
      {
        "drug_id": "DB12345",
        "product_name": "Product A",
        "manufacturer": "Manufacturer A",
        "ndc": "12345",
        "dosage_form": "Tablet",
        "route": "Oral",
        "dosage": "10 mg",
        "country": "USA",
        "regulatory_agency": "FDA"
      },
      {
        "drug_id": "DB12345",
        "product_name": "Product B",
        "manufacturer": "Manufacturer B",
        "ndc": "67890",
        "dosage_form": "Capsule",
        "route": "Oral",
        "dosage": "20 mg",
        "country": "Canada",
        "regulatory_agency": "Health Canada"
      }
    ]
    assert data == expected
    captured = capsys.readouterr().out
    assert "Dane o lekach zapisane do:" in captured