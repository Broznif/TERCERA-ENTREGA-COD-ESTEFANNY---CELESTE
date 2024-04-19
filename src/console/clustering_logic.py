import pandas as pd
import math
import random

def load_data(file_path):
    data = pd.read_csv(file_path, na_values='?', encoding='utf-8')
    data.dropna(inplace=True)
    return data

def select_columns(data, columns):
    return data[columns]

class Clusterer:
    def __init__(self, num_clusters, num_features):
        self.num_clusters = num_clusters
        self.centroids = [[0.0] * num_features for _ in range(num_clusters)]
        self.rnd = random.Random(0)  # Semilla arbitraria

    def cluster(self, data):
        num_tuples = len(data)
        num_values = len(data.columns)
        self.clustering = [i % self.num_clusters for i in range(num_tuples)]
        self.init_random(data)

        changed = True
        max_count = num_tuples * 10
        ct = 0

        while changed and ct <= max_count:
            ct += 1
            self.update_centroids(data)
            changed = self.update_clustering(data)

        result = list(self.clustering)
        return result

    def init_random(self, data):
        num_tuples = len(data)
        cluster_id = 0

        for i in range(num_tuples):
            self.clustering[i] = cluster_id
            cluster_id = (cluster_id + 1) % self.num_clusters

        for i in range(num_tuples):
            r = self.rnd.randint(i, len(self.clustering) - 1)
            tmp = self.clustering[r]
            self.clustering[r] = self.clustering[i]
            self.clustering[i] = tmp

    def update_centroids(self, data):
        cluster_counts = [0] * self.num_clusters

        for i in range(len(data)):
            cluster_id = self.clustering[i]
            cluster_counts[cluster_id] += 1

        for k in range(self.num_clusters):
            for j in range(len(self.centroids[k])):
                self.centroids[k][j] = 0.0

        for i in range(len(data)):
            cluster_id = self.clustering[i]
            for j in range(len(data.columns)):
                value = data.iloc[i, j]
                if isinstance(value, (int, float)):
                    self.centroids[cluster_id][j] += value
                else:
                    self.centroids[cluster_id][j] += 0.0

        for k in range(self.num_clusters):
            for j in range(len(self.centroids[k])):
                if cluster_counts[k] != 0:
                    self.centroids[k][j] /= cluster_counts[k]

    def update_clustering(self, data):
        changed = False
        new_clustering = list(self.clustering)
        distances = [0.0] * self.num_clusters

        for i in range(len(data)):
            for k in range(self.num_clusters):
                distances[k] = self.distance(data.iloc[i], self.centroids[k])

            new_cluster_id = self.min_index(distances)

            if new_cluster_id != new_clustering[i]:
                changed = True
                new_clustering[i] = new_cluster_id

        if not changed:
            return False

        cluster_counts = [0] * self.num_clusters

        for i in range(len(data)):
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

def show_clustered(data, clustering, num_clusters, decimals):
    clusters = {}

    for i, row in enumerate(data.values):
        cluster_id = clustering[i]
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(row)

    result = ""
    for k, rows in clusters.items():
        result += f"===================\n"
        result += f"Cluster {k}:\n"
        for row in rows:
            result += " ".join([f"{value:.{decimals}f}" if isinstance(value, (int, float)) else str(value) for value in row]) + "\n"
        result += f"===================\n"

    return result