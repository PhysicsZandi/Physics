import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

class ER_networks:
    def __init__(self, number_of_nodes, number_of_copies):
        self.number_of_nodes = number_of_nodes
        self.number_of_copies = number_of_copies
        self.critical_probability = 1 / number_of_nodes
        self.copies = []
        self.probabilities = []
        self.number_of_nodes_with_link = []
        self.number_of_links = []
        self.threshold = np.log(number_of_nodes) / number_of_nodes
        self.giant_component = []
        self.giant_component_diameter = []
        self.giant_component_fraction = []
        self.average_degree = []
        self.average_path_length = []

    def set_probabilities(self):
        step = 2 * self.critical_probability / self.number_of_copies 
        prob = self.critical_probability / 2
        for _ in range(self.number_of_copies):
            prob += step
            self.probabilities.append(prob)

    def set_copies(self):
        for p in tqdm(range(len(self.probabilities))):
            adj_matrix = np.zeros((self.number_of_nodes, self.number_of_nodes))
            for i in range(self.number_of_nodes):
                for j in range(self.number_of_nodes):
                    if j > i:
                        adj_matrix[i][j] = np.random.rand()
                        if adj_matrix[i][j] < self.probabilities[p]:
                            adj_matrix[i][j] = 1
                        else:
                            adj_matrix[i][j] = 0
            adj_matrix = adj_matrix + adj_matrix.transpose()
            graph = nx.from_numpy_array(adj_matrix)
            self.copies.append(graph)

    def set_nodes_and_links(self):
        for i in tqdm(range(len(self.copies))):
            adj_matrix = nx.adjacency_matrix(self.copies[i]).toarray()
            arr = list(map(sum, adj_matrix))
            count_n = 0
            count_l = 0
            for i in range(self.number_of_nodes):
                for j in range(self.number_of_nodes):
                    if (j > i) and (adj_matrix[i][j] != 0):
                        count_l += 1
            for i in range(len(arr)): 
                if arr[i] > 0:
                    count_n += 1
            self.number_of_nodes_with_link.append(count_n)
            self.number_of_links.append(count_l)

    def plot_nodes_and_links(self):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].plot(self.probabilities, self.number_of_links), 
        axs[0].set_title("Number of links")
        axs[1].plot(self.probabilities, self.number_of_nodes_with_link), 
        axs[1].set_title("Number of nodes with at least one link")
        fig.tight_layout(pad=2.0)
        plt.show()

    def set_averages(self):
        for i in tqdm(range(len(self.copies))):
            self.average_degree.append(sum(dict(self.copies[i].degree()).values()) / self.number_of_nodes)
            self.average_path_length.append(nx.average_shortest_path_length(self.giant_component[i]))

    def plot_averages(self):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].plot(self.probabilities, self.average_degree), 
        axs[0].set_title("Average degree")
        axs[1].plot(self.probabilities, self.average_path_length), 
        axs[1].set_title("Average shortest path length of the giant component")
        fig.tight_layout(pad=2.0)
        plt.show()

    def plot_networks(self):
        graphs_per_row = 10
        number_of_rows = 1
        if self.number_of_copies >= graphs_per_row:
            number_of_rows = self.number_of_copies // graphs_per_row  
        plt.figure(figsize=(10, 2.5 * number_of_rows))
        for i, graph in enumerate(self.copies):
            plt.subplot(number_of_rows, graphs_per_row, i + 1)
            nx.draw_networkx(graph, node_size=20, with_labels=False)
            plt.title(f"{i + 1}")
        plt.tight_layout(pad=2.0)
        plt.show()

    def print_threshold_and_critical_point(self):
        print(f"The threshold is ", self.threshold)
        print(f"The critical probability is ", self.critical_probability)

    def set_giant_component(self):
        for i in tqdm(range(len(self.copies))):
            connected_subgraphs = sorted(nx.connected_components(self.copies[i]), key=len, reverse=True)
            giant_comp = self.copies[i].subgraph(connected_subgraphs[0])
            self.giant_component.append(giant_comp)
            self.giant_component_diameter.append(nx.diameter(giant_comp))
            self.giant_component_fraction.append(giant_comp.number_of_nodes() / self.number_of_nodes)

    def plot_giant_component_properties(self):
        fig, axs = plt.subplots(1, 2, figsize=(10, 5))
        axs[0].plot(self.probabilities, self.giant_component_diameter), 
        axs[0].set_title("Diameter of the giant component")
        axs[1].plot(self.probabilities, self.giant_component_fraction), 
        axs[1].set_title("Fraction of nodes in the giant component")
        fig.tight_layout(pad=2.0)
        plt.show()

    def plot_giant_components(self):
        graphs_per_row = 10
        number_of_rows = 1
        if self.number_of_copies >= graphs_per_row:
            number_of_rows = self.number_of_copies // graphs_per_row 
        plt.figure(figsize=(10, 2.5 * number_of_rows))
        for i in range(len(self.giant_component)):
            plt.subplot(number_of_rows, graphs_per_row, i + 1)
            node_color = ['blue' if node not in self.giant_component[i] else 'red' for node in self.copies[i].nodes()]
            nx.draw_networkx(self.copies[i], node_color=node_color, node_size=20, with_labels=False)
            plt.title(f"{i + 1}")
        plt.tight_layout(pad=2.0)
        plt.show()