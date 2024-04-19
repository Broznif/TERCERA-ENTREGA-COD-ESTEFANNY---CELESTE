import unittest
import pandas as pd
from unittest.mock import patch
from io import StringIO
from logica.logica import Clusterer, load_data, show_data, show_clustered

class TestClustererErrors(unittest.TestCase):
    """
    This class contains unit tests for error cases in the Clusterer class and related functions.
    """
    # Incorrect number of clusters.
    def test_cluster_invalid_num_clusters(self):
        """
        Test for an invalid number of clusters.
        """
        num_clusters = 'invalido'
        num_features = 5
        data_nuevo = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

        with self.assertRaises(ValueError):  
            clusterer = Clusterer(num_clusters, num_features)
            clusterer.cluster(data_nuevo)

    # Error test for non-numeric data in the clustering function.
    def test_cluster_non_numeric_data(self):
        """
        Test for an error with non-numeric data in the clustering function.
        """
        num_clusters = 3
        num_features = 5
        data_nuevo = pd.DataFrame({'col1': ['a', 'b', 'c'], 'col2': [4, 5, 6]})

        with self.assertRaises(ValueError):  
            clusterer = Clusterer(num_clusters, num_features)
            clusterer.cluster(data_nuevo)
    
    # Error test for distance calculation between data of different dimensions.
    def test_cluster_invalid_distance_calculation(self):
        """
        Test for an error with distance calculation between data of different dimensions.
        """
        num_clusters = 3
        num_features = 5
        data_nuevo = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

        with self.assertRaises(ValueError):  
            clusterer = Clusterer(num_clusters, num_features)
            clusterer.distance(data_nuevo.iloc[0], [1, 2, 3, 4, 5, 6])

    # Error test for an out-of-range index in data visualization.
    def test_show_data_invalid_index(self):
        """
        Test for an error with an out-of-range index in data visualization.
        """
        test_data = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            with self.assertRaises(IndexError):
                show_data(test_data, 1, True, True, indices=True)

if __name__ == '_main_':
    unittest.main()
