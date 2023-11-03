import tempfile
import pytest
from embedchain.loaders.xml import XmlLoader
SAMPLE_XML = '<?xml version="1.0" encoding="UTF-8"?>\n<factbook>\n  <country>\n    <name>United States</name>\n    <capital>Washington, DC</capital>\n    <leader>Joe Biden</leader>\n    <sport>Baseball</sport>\n  </country>\n  <country>\n    <name>Canada</name>\n    <capital>Ottawa</capital>\n    <leader>Justin Trudeau</leader>\n    <sport>Hockey</sport>\n  </country>\n  <country>\n    <name>France</name>\n    <capital>Paris</capital>\n    <leader>Emmanuel Macron</leader>\n    <sport>Soccer</sport>\n  </country>\n  <country>\n    <name>Trinidad &amp; Tobado</name>\n    <capital>Port of Spain</capital>\n    <leader>Keith Rowley</leader>\n    <sport>Track &amp; Field</sport>\n  </country>\n</factbook>'
@pytest.mark.parametrize('xml', [SAMPLE_XML])
def test_load_data(xml: str):
    with tempfile.NamedTemporaryFile(mode='w+') as tmpfile:
        tmpfile.write(xml)
        tmpfile.seek(0)
        filename = tmpfile.name
        loader = XmlLoader()
        result = loader.load_data(filename)
        data = result['data']
        assert len(data) == 4
        assert 'United States Washington, DC Joe Biden' in data[0]['content']
        assert 'Canada Ottawa Justin Trudeau' in data[1]['content']
        assert 'France Paris Emmanuel Macron' in data[2]['content']
        assert 'Trinidad & Tobado Port of Spain Keith Rowley' in data[3]['content']
        assert data[0]['meta_data']['url'] == filename
        assert data[1]['meta_data']['url'] == filename
        assert data[2]['meta_data']['url'] == filename
        assert data[3]['meta_data']['url'] == filename