import unittest
import numpy as np
import pandas as pd
from logica.logica import Clusterer, load_data, show_data, show_clustered

class TestClusterer(unittest.TestCase):
    """
    Test class for the Clusterer class.
    """

    def test_error_cluster_invalid_num_clusters(self):
        """
        Test for an error when attempting to cluster with an invalid number of clusters.
        """
        with self.assertRaises(Exception):
            clusterer = Clusterer(0, 3)

    def test_exception_cluster_invalid_num_clusters(self):
        """
        Test for an exception when attempting to cluster with an invalid number of clusters.
        """
        clusterer = Clusterer(10, 5)
        data_nuevo = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        with self.assertRaises(Exception):
            clusterer.cluster(data_nuevo)

    def test_exception_cluster_insufficient_data(self):
        """
        Test for an exception when attempting to cluster with insufficient data.
        """
        clusterer = Clusterer(5, 5)
        data_nuevo = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
        with self.assertRaises(Exception):
            clusterer.cluster(data_nuevo)

if __name__ == '_main_':
    unittest.main()