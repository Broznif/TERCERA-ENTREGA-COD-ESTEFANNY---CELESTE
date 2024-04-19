import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import math
import random
import sys

''' Load data from a CSV file and preprocess it by removing any rows with missing values. '''
def load_data(file_path):
    data = pd.read_csv(file_path, na_values='?', encoding='utf-8')
    data.dropna(inplace=True)
    return data

''' Select specific columns from the dataset. '''
def select_columns(data, columns):
    return data[columns]

''' Initialize clustering with random assignments to clusters. '''
def init_random(data, num_clusters):
    num_tuples = len(data)
    cluster_id = 0
    clustering = [0] * num_tuples

    for i in range(num_tuples):
        clustering[i] = cluster_id
        cluster_id = (cluster_id + 1) % num_clusters

    for i in range(num_tuples):
        r = random.randint(i, len(clustering) - 1)
        tmp = clustering[r]
        clustering[r] = clustering[i]
        clustering[i] = tmp

    return clustering

class Clusterer:
    ''' Initialize the Clusterer object with the number of clusters and features. '''
    def __init__(self, num_clusters, num_features):
        self.num_clusters = num_clusters
        self.centroids = [[0.0] * num_features for _ in range(num_clusters)]
        self.rnd = random.Random(0)  # Arbitrary seed

    ''' Perform k-means clustering on the given data. '''
    def cluster(self, data_nuevo):
        num_tuples = len(data_nuevo)
        num_values = len(data_nuevo.columns)
        self.clustering = [i % self.num_clusters for i in range(num_tuples)]
        self.init_random(data_nuevo)

        print("\nInitial random clustering:")
        print(" ".join(map(str, self.clustering)) + "\n")

        changed = True
        max_count = num_tuples * 10
        ct = 0

        while changed and ct <= max_count:
            ct += 1
            self.update_centroids(data_nuevo)
            changed = self.update_clustering(data_nuevo)

        result = list(self.clustering)
        return result

    ''' Initialize clustering randomly. '''
    def init_random(self, data_nuevo):
        num_tuples = len(data_nuevo)
        cluster_id = 0

        for i in range(num_tuples):
            self.clustering[i] = cluster_id
            cluster_id = (cluster_id + 1) % self.num_clusters

        for i in range(num_tuples):
            r = self.rnd.randint(i, len(self.clustering) - 1)
            tmp = self.clustering[r]
            self.clustering[r] = self.clustering[i]
            self.clustering[i] = tmp

    ''' Update cluster centroids based on current clustering. '''
    def update_centroids(self, data_nuevo):
        cluster_counts = [0] * self.num_clusters

        for i in range(len(data_nuevo)):
            cluster_id = self.clustering[i]
            cluster_counts[cluster_id] += 1

        for k in range(self.num_clusters):
            for j in range(len(self.centroids[k])):
                self.centroids[k][j] = 0.0

        for i in range(len(data_nuevo)):
            cluster_id = self.clustering[i]
            for j in range(len(data_nuevo.columns)):
                value = data_nuevo.iloc[i, j]
                if isinstance(value, (int, float)):
                    self.centroids[cluster_id][j] += value
                else:
                    self.centroids[cluster_id][j] += 0.0

        for k in range(self.num_clusters):
            for j in range(len(self.centroids[k])):
                if cluster_counts[k] != 0:
                    self.centroids[k][j] /= cluster_counts[k]

    ''' Update cluster assignments based on current centroids. '''
    def update_clustering(self, data_nuevo):
        changed = False
        new_clustering = list(self.clustering)
        distances = [0.0] * self.num_clusters

        for i in range(len(data_nuevo)):
            for k in range(self.num_clusters):
                distances[k] = self.distance(data_nuevo.iloc[i], self.centroids[k])

            new_cluster_id = self.min_index(distances)

            if new_cluster_id != new_clustering[i]:
                changed = True
                new_clustering[i] = new_cluster_id

        if not changed:
            return False

        cluster_counts = [0] * self.num_clusters

        for i in range(len(data_nuevo)):
            cluster_id = new_clustering[i]
            cluster_counts[cluster_id] += 1

        for k in range(self.num_clusters):
            if cluster_counts[k] == 0:
                return False

        self.clustering = list(new_clustering)
        return True

    ''' Calculate the distance between a data point and a centroid. '''
    @staticmethod
    def distance(tuple, centroid):
        sum_squared_diffs = sum((float(tuple[j]) - centroid[j]) ** 2 if isinstance(tuple[j], (int, float)) else 0.0 for j in range(len(tuple)))
        return math.sqrt(sum_squared_diffs)

    ''' Find the index of the minimum distance in a list of distances. '''
    @staticmethod
    def min_index(distances):
        index_of_min = 0
        small_dist = distances[0]

        for k in range(1, len(distances)):
            if distances[k] < small_dist:
                small_dist = distances[k]
                index_of_min = k

        return index_of_min

    ''' Display the clustered data. '''
    def show_clustered(data_nuevo, clustering, num_clusters, decimals):
        clusters = {}

        # Organize data by clusters
        for i, row in enumerate(data_nuevo.values):
            cluster_id = clustering[i]
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(row)

        # Construct text to display clusters
        result_text = ""
        for k, rows in clusters.items():
            result_text += f"===================\nCluster {k}:\n"
            for row in rows:
                result_text += " ".join([f"{value:.{decimals}f}" if isinstance(value, (int, float)) else str(value) for value in row]) + "\n"
            result_text += "===================\n"

        # Display the text
        print(result_text)

def main():
    print("\nBegin k-means clustering demo\n")

    file_path = input("Enter the path to the CSV file: ")
    data = load_data(file_path)

    num_clusters = int(input("Enter the number of clusters: "))
    print(f"\nSetting numClusters to {num_clusters}")

    print("Raw unclustered data:\n")
    print(data)

    print("Starting clustering using k-means algorithm")

    clusterer = Clusterer(num_clusters, len(data.columns))
    clustering_result = clusterer.cluster(data)

    print("Clustering complete\n")

    print("Clustered data:\n")
    Clusterer.show_clustered(data, clustering_result, num_clusters, 1)

if __name__ == "__main__":
    main()