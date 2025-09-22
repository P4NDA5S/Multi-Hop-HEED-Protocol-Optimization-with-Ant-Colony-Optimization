import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

class WSN:
    def __init__(self, num_nodes, area_size=100, init_energy=1.0):
        self.num_nodes = num_nodes
        self.area_size = area_size
        self.init_energy = init_energy
        self.pos = np.random.rand(num_nodes, 2) * area_size
        self.clusters = np.zeros(num_nodes, dtype=int)
        self.energy = np.ones(num_nodes) * init_energy  # energi per node

    def plot_clusters(self, title="Clustering HEED", ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        # warna berbeda per cluster
        unique_clusters = np.unique(self.clusters)
        for cluster_id in unique_clusters:
            nodes = np.where(self.clusters == cluster_id)[0]
            ax.scatter(self.pos[nodes, 0], self.pos[nodes, 1], label=f"Cluster {cluster_id}")

        ax.set_title(title)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()

    def plot_routing(self, path, title="Routing ACO", ax=None):
        if ax is None:
            fig, ax = plt.subplots()
        xs, ys = self.pos[path, 0], self.pos[path, 1]
        ax.plot(xs, ys, "r-o")
        ax.set_title(title)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

    def build_graph(self):
        G = nx.Graph()
        for i in range(self.num_nodes):
            for j in range(i+1, self.num_nodes):
                dist = np.linalg.norm(self.pos[i] - self.pos[j])
                G.add_edge(i, j, weight=dist)
        return G

    def simulate_transmission(self, path):
        energies = []
        avg_energy = self.init_energy

        for r in range(10):  # contoh 10 round
            # setiap hop konsumsi energi
            cost = 0.01 * len(path)
            self.energy[path] -= cost
            self.energy = np.maximum(self.energy, 0)
            avg_energy = np.mean(self.energy)
            energies.append(avg_energy)

        return energies