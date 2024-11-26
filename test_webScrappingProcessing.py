import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import os
from webScrappingProcessing import get_sample_links, extract_sample_data, update_csv_file

class TestWebScrapingAndCSVUpdate(unittest.TestCase):
    def setUp(self):
        # Prepare mock data
        self.mock_sample_links = [
            {"sample_id": "GSM12345", "url": "http://mock-url-1"},
            {"sample_id": "GSM67890", "url": "http://mock-url-2"}
        ]
        self.mock_sample_data = [
            {"id_ref": "Sample1", "case_control": "Case"},
            {"id_ref": "Sample2", "case_control": "Control"}
        ]
        self.input_file = "test_samples_case_control.csv"
        self.output_file = "test_updated_samples_case_control.csv"
        pd.DataFrame(self.mock_sample_data).to_csv(self.input_file, index=False)

    def test_get_sample_links(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = '<a href="/geo/query/GSM12345">GSM12345</a>'
            sample_links = get_sample_links("http://mock-url")
            self.assertEqual(len(sample_links), 1)
            self.assertEqual(sample_links[0]["sample_id"], "GSM12345")

    def test_extract_sample_data(self):
        with patch("requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = """
                <td>Title</td><td>Sample1</td>
                <td>Characteristics</td><td>case_control: Case</td>
            """
            sample_data = extract_sample_data(self.mock_sample_links[0])
            self.assertEqual(sample_data["id_ref"], "Sample1")
            self.assertEqual(sample_data["case_control"], "Case")

    def test_update_csv_file(self):
        update_csv_file(self.input_file, self.output_file)
        df = pd.read_csv(self.output_file)
        self.assertEqual(df.iloc[0]["case_control"], "Progressor")
        self.assertEqual(df.iloc[1]["case_control"], "Non-progressor")

    def tearDown(self):
        if os.path.exists(self.input_file):
            os.remove(self.input_file)
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

if __name__ == "__main__":
    unittest.main()
