import os
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex8 import task_8

SAMPLE_XML_TASK8 = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2006-01-01" updated="2024-01-02">
    <drugbank-id primary="true">DB00020</drugbank-id>
    <targets>
      <target>
         <id>TARGET001</id>
         <polypeptide id="P00010" source="UniProtKB">
            <name>Protein X</name>
            <gene-name>GENEX</gene-name>
            <cellular-location>Membrane</cellular-location>
         </polypeptide>
      </target>
      <target>
         <id>TARGET002</id>
         <polypeptide id="P00011" source="UniProtKB">
            <name>Protein Y</name>
            <gene-name>GENEY</gene-name>
         </polypeptide>
      </target>
    </targets>
  </drug>
</drugbank>
'''

def test_task_8(tmp_path, capsys):
    xml_file = tmp_path / "sample_task8.xml"
    xml_file.write_text(SAMPLE_XML_TASK8, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_8(str(xml_file), str(output_dir))
    output_file = output_dir / "ex8_targets_cellular_location_pie_chart.png"
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    captured = capsys.readouterr().out
    assert "Pie chart saved to:" in captured
