# aco.py
import numpy as np
import random


class AntColony:
    def __init__(self, graph, n_ants, n_iterations, decay, alpha=1, beta=2):
        """
        :param graph: Graph NetworkX dengan bobot edge
        :param n_ants: jumlah semut
        :param n_iterations: jumlah iterasi
        :param decay: faktor penguapan feromon
        :param alpha: pengaruh feromon
        :param beta: pengaruh jarak
        """
        self.graph = graph
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

        n_nodes = len(graph.nodes)
        self.pheromone = np.ones((n_nodes, n_nodes))  # matriks feromon

    def _probability(self, current, unvisited):
        pheromone = self.pheromone[current, unvisited] ** self.alpha
        distance = np.array([self.graph[current][j]['weight'] for j in unvisited])
        distance[distance == 0] = 1e-6  # cegah div 0
        heuristic = (1.0 / distance) ** self.beta
        prob = pheromone * heuristic
        prob_sum = prob.sum()
        if prob_sum == 0:
            return np.ones_like(prob) / len(prob)
        return prob / prob_sum

    def _build_path(self, start, end):
        path = [start]
        visited = set(path)
        current = start
        while current != end:
            unvisited = [n for n in self.graph.nodes if n not in visited]
            if not unvisited:
                break
            probs = self._probability(current, unvisited)
            next_node = np.random.choice(unvisited, p=probs)
            path.append(next_node)
            visited.add(next_node)
            current = next_node
        return path

    def run(self, start, end):
        best_path = None
        best_cost = float("inf")

        for _ in range(self.n_iterations):
            all_paths = []
            all_costs = []

            for _ in range(self.n_ants):
                path = self._build_path(start, end)
                cost = sum(self.graph[path[i]][path[i+1]]['weight']
                           for i in range(len(path)-1))
                all_paths.append(path)
                all_costs.append(cost)

                if cost < best_cost:
                    best_path = path
                    best_cost = cost

            # Update feromon
            self.pheromone *= (1 - self.decay)
            for path, cost in zip(all_paths, all_costs):
                for i in range(len(path)-1):
                    self.pheromone[path[i]][path[i+1]] += 1.0 / cost

        return best_path, best_cost