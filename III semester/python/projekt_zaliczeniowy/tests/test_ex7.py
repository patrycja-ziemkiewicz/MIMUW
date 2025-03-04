import os
import json
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex7 import task_7

SAMPLE_XML_TARGETS = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB00010</drugbank-id>
    <targets>
      <target>
        <id>TARGET001</id>
        <polypeptide id="P00001" source="UniProtKB">
          <name>Protein A</name>
          <gene-name>GENE_A</gene-name>
          <chromosome-location>1</chromosome-location>
          <cellular-location>Nucleus</cellular-location>
          <external-identifiers>
            <external-identifier>
              <resource>GenAtlas</resource>
              <identifier>GA001</identifier>
            </external-identifier>
          </external-identifiers>
        </polypeptide>
      </target>
    </targets>
  </drug>
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB00011</drugbank-id>
  </drug>
</drugbank>
'''

def test_task_7(tmp_path, capsys):
    xml_file = tmp_path / "sample_targets.xml"
    xml_file.write_text(SAMPLE_XML_TARGETS, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_7(str(xml_file), str(output_dir))
    json_file = output_dir / "ex7.json"
    assert json_file.exists()
    with json_file.open("r", encoding="utf-8") as f:
        data = json.load(f)
    expected = [{
        "target_drugbank_id": "TARGET001",
        "source": "UniProtKB",
        "external_id": "P00001",
        "polypeptide_name": "Protein A",
        "gene_name": "GENE_A",
        "genatlas_id": "GA001",
        "chromosome": "1",
        "cellular_location": "Nucleus"
    }]
    assert data == expected
    captured = capsys.readouterr().out
    assert "Dane o targetach zapisane do:" in captured
