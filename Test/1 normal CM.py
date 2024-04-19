from logica.logica import Clusterer, load_data, show_data, show_clustered 
import unittest
import pandas as pd

class TestClusterer(unittest.TestCase):
    def setUp(self):
        """
        Common setup for the tests.
        """
        self.num_clusters = 3
        self.input_file = "adults.csv"  
        self.raw_data = load_data(self.input_file)
        self.clusterer = Clusterer(self.num_clusters, len(self.raw_data.columns))

    def test_cluster(self):
        """
        Test the 'cluster' method of the Clusterer class.
        """
        clustering_result = self.clusterer.cluster(self.raw_data)
        self.assertEqual(len(clustering_result), len(self.raw_data))

    def test_load_data(self):
        """
        Test the 'load_data' function.
        """
        data = load_data(self.input_file)
        self.assertIsNotNone(data)

    def test_show_data(self):
        """
        Test the 'show_data' function.
        """
        with self.assertLogs() as logs:
            show_data(self.raw_data, decimals=2, indices=True, new_line=True)
        self.assertTrue(logs.output)  # Verify that logs are generated

    def test_distance_calculation(self):
        """
        Test the calculation of Euclidean distance between two tuples (vectors) of data.
        """
        tuple1 = pd.Series([1, 2, 3, 4, 5])
        tuple2 = pd.Series([2, 3, 4, 5, 6])
        distance = Clusterer.distance(tuple1, tuple2)
        self.assertEqual(distance, 2.23606797749979)  
    
    def test_min_index_calculation(self):
        """
        Test the 'min_index' function in the Clusterer class.
        """
        distances = [3.5, 1.2, 5.0, 2.0]
        min_index = Clusterer.min_index(distances)
        self.assertEqual(min_index, 1)  

    def test_show_clustered(self):
        """
        Test the 'show_clustered' function.
        """
        clustering_result = self.clusterer.cluster(self.raw_data)
        with self.assertLogs() as logs:
            show_clustered(self.raw_data, clustering_result, self.num_clusters, decimals=2)
        self.assertTrue(logs.output)  # Verify that logs are generated

if __name__ == '_main_':
    unittest.main()