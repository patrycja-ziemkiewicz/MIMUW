import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex6 import task_6

SAMPLE_XML_TASK6 = '''<?xml version="1.0" encoding="UTF-8"?>
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
        <drugbank-id>DB00001</drugbank-id>
      </drug>
      <drug>
        <drugbank-id>DB00003</drugbank-id>
      </drug>
    </drugs>
  </pathway>
</drugbank>
'''

def test_task_6(tmp_path, capsys):
    xml_file = tmp_path / "sample_task6.xml"
    xml_file.write_text(SAMPLE_XML_TASK6, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_6(str(xml_file), str(output_dir))
    json_file = output_dir / "ex6.json"
    assert json_file.exists()
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    expected = [
        {"drug_id": "DB00001", "pathway_count": 2},
        {"drug_id": "DB00002", "pathway_count": 1},
        {"drug_id": "DB00003", "pathway_count": 1}
    ]
    sorted_data = sorted(data, key=lambda x: x["drug_id"])
    sorted_expected = sorted(expected, key=lambda x: x["drug_id"])
    assert sorted_data == sorted_expected
    histogram_file = output_dir / "ex6_drug_pathway_histogram.png"
    assert histogram_file.exists()
    assert histogram_file.stat().st_size > 0
    captured = capsys.readouterr().out
    assert "Dane o liczbie szlaków dla leków zapisane do:" in captured
    assert "Bar chart saved to:" in captured
