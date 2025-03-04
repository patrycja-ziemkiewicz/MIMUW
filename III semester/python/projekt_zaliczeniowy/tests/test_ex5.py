import os
import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ex5 import task_5

SAMPLE_XML_BIPARTITE = '''<?xml version="1.0" encoding="UTF-8"?>
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
                <drugbank-id>DB00003</drugbank-id>
            </drug>
        </drugs>
    </pathway>
</drugbank>
'''

def test_task_5(tmp_path, capsys):
    xml_file = tmp_path / "sample_bipartite.xml"
    xml_file.write_text(SAMPLE_XML_BIPARTITE, encoding="utf-8")
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    task_5(str(xml_file), str(output_dir))
    output_file = output_dir / "ex5_bipartite_graph.png"
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    captured = capsys.readouterr().out
    assert "Bipartite graph saved to:" in captured
