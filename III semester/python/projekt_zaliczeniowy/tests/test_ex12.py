import os
import pytest
import sys
import imageio
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex12 import task_12

def fake_requests_get_secreted(url, headers, timeout):
    class FakeResponse:
        def __init__(self, content):
            self.content = content
        def raise_for_status(self):
            pass
    fake_xml = '''<entry xmlns="http://uniprot.org/uniprot">
        <comment type="subcellular location">
            <text>Secreted</text>
        </comment>
    </entry>'''
    return FakeResponse(fake_xml.encode("utf-8"))

def fake_requests_get_error(url, headers, timeout):
    raise Exception("Simulated API error")

SAMPLE_XML_TASK12 = '''<?xml version="1.0" encoding="UTF-8"?>
<drugbank xmlns="http://www.drugbank.ca">
  <drug type="chemical" created="2006-01-01" updated="2024-01-01">
    <drugbank-id primary="true">DB010</drugbank-id>
    <targets>
      <target>
         <id>TARGET100</id>
         <polypeptide id="P12345" source="UniProtKB">
            <name>Protein X</name>
            <gene-name>GENEX</gene-name>
            <cellular-location>Some Location</cellular-location>
            <external-identifiers>
                <external-identifier>
                   <resource>UniProtKB</resource>
                   <identifier>P12345</identifier>
                </external-identifier>
            </external-identifiers>
         </polypeptide>
      </target>
    </targets>
  </drug>
</drugbank>
'''

def test_task_12_api_valid(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr("ex12.requests.get", fake_requests_get_secreted)
    xml_file = tmp_path / "sample_task12_valid.xml"
    xml_file.write_text(SAMPLE_XML_TASK12, encoding="utf-8")
    output_dir = tmp_path / "output_valid"
    output_dir.mkdir()
    task_12(str(xml_file), str(output_dir))
    output_file = output_dir / "ex12_two_pies.png"
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    captured = capsys.readouterr().out
    assert "Two pie charts saved to:" in captured

def test_task_12_api_error(monkeypatch, tmp_path, capsys):
    monkeypatch.setattr("ex12.requests.get", fake_requests_get_error)
    xml_file = tmp_path / "sample_task12_error.xml"
    xml_file.write_text(SAMPLE_XML_TASK12, encoding="utf-8")
    output_dir = tmp_path / "output_error"
    output_dir.mkdir()
    task_12(str(xml_file), str(output_dir))
    output_file = output_dir / "ex12_two_pies.png"
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    captured = capsys.readouterr().out
    assert "Two pie charts saved to:" in captured
