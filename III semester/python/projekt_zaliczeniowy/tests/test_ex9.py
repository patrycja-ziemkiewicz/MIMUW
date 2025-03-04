import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex9 import task_9

SAMPLE_XML_TASK9 = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB001</drugbank-id>
    <name>Drug One</name>
    <groups>
      <group>approved</group>
      <group>other</group>
    </groups>
  </drug>
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB002</drugbank-id>
    <name>Drug Two</name>
    <groups>
      <group>approved</group>
      <group>withdrawn</group>
    </groups>
  </drug>
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB003</drugbank-id>
    <name>Drug Three</name>
    <groups>
      <group>experimental</group>
    </groups>
  </drug>
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB004</drugbank-id>
    <name>Drug Four</name>
    <groups>
      <group>vet_approved</group>
    </groups>
  </drug>
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB005</drugbank-id>
    <name>Drug Five</name>
    <groups>
      <group>investigational</group>
    </groups>
  </drug>
</drugbank>
'''

def test_task_9(tmp_path, capsys):
    xml_file = tmp_path / "sample_task9.xml"
    xml_file.write_text(SAMPLE_XML_TASK9, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_9(str(xml_file), str(output_dir))
    json_file = output_dir / "ex9.json"
    assert json_file.exists()
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    expected = [
      {"Status": "approved", "Count": 2},
      {"Status": "withdrawn", "Count": 1},
      {"Status": "experimental/investigational", "Count": 2},
      {"Status": "vet_approved", "Count": 1}
    ]
    sorted_data = sorted(data, key=lambda x: x["Status"])
    sorted_expected = sorted(expected, key=lambda x: x["Status"])
    assert sorted_data == sorted_expected
    pie_chart_file = output_dir / "ex9_drug_status_pie_chart.png"
    assert pie_chart_file.exists()
    captured = capsys.readouterr().out
    assert "Status summary saved to:" in captured
    assert "Pie chart saved to:" in captured
    assert "Liczba zatwierdzonych leków, które nie zostały wycofane:" in captured
    assert "1" in captured
