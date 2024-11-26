import unittest
import pandas as pd
from io import StringIO

class TestDataProcessing(unittest.TestCase):
    def setUp(self):
        # Mock data for testing
        self.mock_main_data = StringIO(
            """id_ref,cg12374721,cg18081940,cg04475027,case_control
            sample1,0.5,0.6,0.7,Progressor
            sample2,0.2,0.3,0.4,Non-progressor
            sample3,0.1,0.2,0.3,Progressor
            sample4,0.4,0.5,0.6,Non-progressor"""
        )
        self.cpg_sites = ['id_ref', 'cg12374721', 'cg18081940', 'cg04475027']

    def test_progressing_subsetting(self):
        # Read mock data
        mock_df = pd.read_csv(self.mock_main_data)
        
        # Subset mock data
        progressing = mock_df[mock_df['case_control'] == 'Progressor']
        non_progressing = mock_df[mock_df['case_control'] == 'Non-progressor']
        
        # Verify subsets
        self.assertEqual(len(progressing), 2)
        self.assertEqual(len(non_progressing), 2)
        self.assertTrue((progressing['case_control'] == 'Progressor').all())
        self.assertTrue((non_progressing['case_control'] == 'Non-progressor').all())

if __name__ == '__main__':
    unittest.main()
