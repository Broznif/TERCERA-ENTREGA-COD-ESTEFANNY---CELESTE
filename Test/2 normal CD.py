import unittest
import pandas as pd
from io import StringIO
from unittest.mock import patch
from logica.logica import Clusterer, load_data, show_data, show_clustered

class TestDataLoading(unittest.TestCase):
    """
    This class contains unit tests for data loading functions.
    """
    # Test data loading from a simulated CSV file and verify that the result is a Pandas DataFrame with the expected structure and data quantity.
    def test_load_data(self):
        """
        Test data loading from a simulated CSV file.
        """
        # Create a temporary CSV file to test data loading
        test = 'age,educational-num,capital-gain,capital-loss,hours-per-week\n25,12,5000,200,40\n30,14,6000,150,45\n'
        with patch('builtins.open', return_value=StringIO(test)):
            loaded_data = load_data('test.csv')

        self.assertIsInstance(loaded_data, pd.DataFrame)
        self.assertEqual(len(loaded_data), 2)

    # Verify that the show_data function produces the expected output when a specific DataFrame is passed to it.
    def test_show_data(self):
        """
        Test the show_data function output with a specific DataFrame.
        """
        test_data = pd.DataFrame({
            'age': [25, 30],
            'educational-num': [12, 14],
            'capital-gain': [5000, 6000],
            'capital-loss': [200, 150],
            'hours-per-week': [40, 45]
        })

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            show_data(test_data, 1, True, True)

        result = mock_stdout.getvalue()
        expected_output = "0   25.0    12.0    5000.0    200.0    40.0    \n1   30.0    14.0    6000.0    150.0    45.0    \n"

        self.assertEqual(result, expected_output)   
    
    # Simulate data loading from a CSV file containing additional information.
    def test_load_data_normal_case(self):
        """
        Test normal case data loading from a CSV file with additional information.
        """
        # Create a temporary CSV file with additional data
        test_normal = 'age,educational-num,capital-gain,capital-loss,hours-per-week\n35,16,8000,100,50\n40,18,10000,50,55\n'
        with patch('builtins.open', return_value=StringIO(test_normal)):
            loaded_data = load_data('test_normal.csv')
        self.assertIsInstance(loaded_data, pd.DataFrame)
        self.assertEqual(len(loaded_data), 2)    

if __name__ == '_main_':
    unittest.main()