import os
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex11 import task_11

SAMPLE_XML_TASK11 = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2000-01-01" updated="2024-01-01">
    <drugbank-id primary="true">DB00002</drugbank-id>
    <name>TestDrugF2</name>
    <targets>
      <target>
         <id>TARGETF2</id>
         <polypeptide id="P_F2" source="UniProtKB">
           <name>Protein F2</name>
           <gene-name>F2</gene-name>
           <cellular-location>Extracellular</cellular-location>
           <external-identifiers>
              <external-identifier>
                <resource>UniProtKB</resource>
                <identifier>P_F2</identifier>
              </external-identifier>
           </external-identifiers>
         </polypeptide>
      </target>
    </targets>
    <products>
      <product>
         <name>Product X</name>
         <labeller>Manufacturer X</labeller>
         <ndc-product-code>11111</ndc-product-code>
         <dosage-form>Injection</dosage-form>
         <route>IV</route>
         <strength>5 mg</strength>
         <country>USA</country>
         <source>FDA</source>
      </product>
    </products>
  </drug>
</drugbank>
'''

def test_task_11(tmp_path, capsys):
    xml_file = tmp_path / "sample_task11.xml"
    xml_file.write_text(SAMPLE_XML_TASK11, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_11(str(xml_file), str(output_dir))
    output_gif = output_dir / "ex11_gene_F2_animation.gif"
    assert output_gif.exists()
    assert output_gif.stat().st_size > 0
    captured = capsys.readouterr().out
    assert "Animowany GIF zapisany do:" in captured
