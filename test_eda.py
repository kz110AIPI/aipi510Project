import unittest
import pandas as pd
from scipy.stats import ttest_ind
import os

class TestCpGAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load test datasets
        cls.non_progressing_df = pd.read_csv('non_progressing_subset.csv')
        cls.progressing_df = pd.read_csv('progressing_subset.csv')
        cls.cpg_sites = ['cg12374721', 'cg18081940', 'cg04475027']
    
    def test_data_load(self):
        # Test if data is loaded correctly
        self.assertFalse(self.non_progressing_df.empty, "Non-progressing dataset is empty.")
        self.assertFalse(self.progressing_df.empty, "Progressing dataset is empty.")
    
    def test_cpg_sites_presence(self):
        # Test if CpG sites are present in the datasets
        for cpg in self.cpg_sites:
            self.assertIn(cpg, self.non_progressing_df.columns, f"{cpg} missing in non-progressing dataset.")
            self.assertIn(cpg, self.progressing_df.columns, f"{cpg} missing in progressing dataset.")
    
    def test_ttest_ind(self):
        # Test t-test for a CpG site
        cpg = self.cpg_sites[0]
        t_stat, p_val = ttest_ind(
            self.non_progressing_df[cpg], 
            self.progressing_df[cpg], 
            nan_policy='omit'
        )
        self.assertIsInstance(t_stat, float, "T-statistic is not a float.")
        self.assertIsInstance(p_val, float, "P-value is not a float.")
    
    def test_combined_dataframe(self):
        # Test the combined dataframe structure
        combined_df = pd.concat([
            self.non_progressing_df[self.cpg_sites].assign(Group='Non-Progressing'),
            self.progressing_df[self.cpg_sites].assign(Group='Progressing')
        ])
        self.assertIn('Group', combined_df.columns, "'Group' column missing in combined dataframe.")
        self.assertEqual(len(combined_df), len(self.non_progressing_df) + len(self.progressing_df), 
                         "Combined dataframe length mismatch.")
    
    def test_statistical_results_save(self):
        # Test if results are saved correctly
        results = []
        for cpg in self.cpg_sites:
            t_stat, p_val = ttest_ind(
                self.non_progressing_df[cpg], 
                self.progressing_df[cpg], 
                nan_policy='omit'
            )
            results.append({'CpG Site': cpg, 'T-Statistic': t_stat, 'P-Value': p_val})
        
        results_df = pd.DataFrame(results)
        results_path = 'cpg_sites_statistical_results_test.csv'
        results_df.to_csv(results_path, index=False)
        self.assertTrue(os.path.exists(results_path), "Results file was not created.")
        os.remove(results_path)

if __name__ == '__main__':
    unittest.main()
