import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex10 import task_10

SAMPLE_XML_INTERACTIONS = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2000-01-01" updated="2024-01-01">
    <drugbank-id primary="true">DB00002</drugbank-id>
    <drug-interactions>
      <drug-interaction>
         <drugbank-id>DB11111</drugbank-id>
         <name>Interaction Drug A</name>
         <description>Increases effect.</description>
      </drug-interaction>
      <drug-interaction>
         <drugbank-id>DB22222</drugbank-id>
         <name>Interaction Drug B</name>
         <description>Decreases effect.</description>
      </drug-interaction>
    </drug-interactions>
  </drug>
  <drug type="chemical" created="2000-01-01" updated="2024-01-01">
    <drugbank-id primary="true">DB00003</drugbank-id>
    <drug-interactions>
      <drug-interaction>
         <drugbank-id>DB33333</drugbank-id>
         <name>Interaction Drug C</name>
         <description>Neutral effect.</description>
      </drug-interaction>
    </drug-interactions>
  </drug>
</drugbank>
'''

def test_task_10(tmp_path, capsys):
    xml_file = tmp_path / "sample_interactions.xml"
    xml_file.write_text(SAMPLE_XML_INTERACTIONS, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_10(str(xml_file), str(output_dir))
    json_file = output_dir / "ex10.json"
    assert json_file.exists()
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    expected = [
        {
            "drug_id": "DB00002",
            "interacting_drugbank_id": "DB11111",
            "interacting_drug_name": "Interaction Drug A",
            "interaction_description": "Increases effect."
        },
        {
            "drug_id": "DB00002",
            "interacting_drugbank_id": "DB22222",
            "interacting_drug_name": "Interaction Drug B",
            "interaction_description": "Decreases effect."
        }
    ]
    assert data == expected
    captured = capsys.readouterr().out
    assert "Dane o interakcjach dla leku DB00002 zapisane do:" in captured
