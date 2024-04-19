import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import math
import random
import sys
warnings.filterwarnings('ignore')

"""
Load data
"""
data = pd.read_csv(r'C:\Users\User\Downloads\PRIMERA ENTREA COD ESTEFANNY - CELESTE\src\console\adult.csv', na_values='?', encoding='utf-8')
data.dropna(inplace=True) 

"""
Select columns from working directory
"""
selected_columns = ['age', 'educational-num', 'capital-gain', 'capital-loss', 'hours-per-week']
data_selected = data[selected_columns]

"""
Max 400 data rows
"""
data_nuevo = data_selected.head(400)

print(data_nuevo)
data_nuevo.head()

# - - - - - - - - - - - - - - - - - - - -

class Clusterer:
    def __init__(self, num_clusters, num_features):
        self.num_clusters = num_clusters
        self.centroids = [[0.0] * num_features for _ in range(num_clusters)]
        self.rnd = random.Random(0)  # Semilla arbitraria

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

    @staticmethod
    def distance(tuple, centroid):
        sum_squared_diffs = sum((float(tuple[j]) - centroid[j]) ** 2 if isinstance(tuple[j], (int, float)) else 0.0 for j in range(len(tuple)))
        return math.sqrt(sum_squared_diffs)


    @staticmethod
    def min_index(distances):
        index_of_min = 0
        small_dist = distances[0]

        for k in range(1, len(distances)):
            if distances[k] < small_dist:
                small_dist = distances[k]
                index_of_min = k

        return index_of_min

def show_clustered(data_nuevo, clustering, num_clusters, decimals):
    for k in range(num_clusters):
        print("===================")
        for i, row in enumerate(data_nuevo.values):
            cluster_id = clustering[i]
            if cluster_id != k:
                continue
            print(f"{i:3} ", end="")
            for value in row:
                if isinstance(value, (int, float)):
                    print(f"{value:.{decimals}f} ", end="")
                else:
                    print(f"{value} ", end="")
            print("")
        print("===================")

def main():
    print("\nBegin k-means clustering demo\n")

    # Parámetros configurados directamente en el código
    num_clusters = 3

    print("Raw unclustered  data_nuevo:\n")
    print(" ")
    print("---------------------")
    print(data_nuevo)

    print(f"\nSetting numClusters to {num_clusters}")
    print("Starting clustering using k-means algorithm")

    clusterer = Clusterer(num_clusters, len(data_nuevo.columns))
    clustering_result = clusterer.cluster(data_nuevo)

    print("Clustering complete\n")

    print("Clustered data_nuevo:\n")
    print("===================")
    show_clustered(data_nuevo, clustering_result, num_clusters, 1)

if __name__ == "__main__":
    main()