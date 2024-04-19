import unittest
import pandas as pd
from unittest.mock import patch
from io import StringIO
from logica.logica import Clusterer, load_data, show_data, show_clustered

class TestLoadDataExceptions(unittest.TestCase):
    """
    This class contains unit tests for exception cases in the data loading and visualization functions.
    """

    # Exception test for invalid data in show_data.
    def test_show_data_invalid_data(self):
        """
        Test for an exception with invalid data in the show_data function.
        """
        invalid_data = 'invalid_data'
        with self.assertRaises(Exception):  
            show_data(invalid_data, 1, True, True)

    # Exception test for file not found during data loading.
    def test_load_data_file_not_found(self):
        """
        Test for an exception with file not found during data loading.
        """
        with self.assertRaises(FileNotFoundError):
            load_data('nonexistent_file.csv')

    # Exception test for invalid data in show_clustered.
    def test_show_clustered_invalid_data(self):
        """
        Test for an exception with invalid data in the show_clustered function.
        """
        invalid_data = 'invalid_data'
        clustering_result = [0, 1, 2]
        with self.assertRaises(Exception):  
            show_clustered(invalid_data, clustering_result, 3, 1)

    # Capture standard output during the execution of show_clustered and compare it with the expected output
    # to verify that the function produces the correct output given the input data and clustering result.
    def test_show_clustered(self):
        """
        Test for show_clustered function with a specific input and clustering result.
        """
        test_data = pd.DataFrame({
            'age': [25, 30, 35, 40, 45, 50, 55, 60],
            'educational-num': [12, 14, 16, 18, 20, 22, 24, 26],
            'capital-gain': [5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000],
            'capital-loss': [200, 150, 100, 50, 0, 50, 100, 150],
            'hours-per-week': [40, 45, 50, 55, 60, 65, 70, 75]
        })

        clustering_result = [0, 1, 2, 0, 1, 2, 0, 1]  # Example clustering result

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            show_clustered(test_data, clustering_result, 3, 1)

        result = mock_stdout.getvalue()
        expected_output = "===================\n0   25.0    12.0    5000.0    200.0    40.0    \n3   40.0    18.0    8000.0    50.0    55.0    \n6   55.0    24.0    11000.0    100.0    70.0    \n===================\n"

if __name__ == '_main_':
    unittest.main()