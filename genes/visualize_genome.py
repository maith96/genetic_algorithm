import numpy as np
from genes.genome import Genome

import networkx as nx
import matplotlib.pyplot as plt


class VisualizeGenome:
    def __init__(self, genome: Genome) -> None:
        self.genome = genome
        self.graph = nx.DiGraph()
        self.create_graph()
        self.draw()
    
    def draw(self):
        pos = nx.spring_layout(self.graph)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        node_labels = {i: f'{i}\nT: {self.graph.nodes[i]["threshold"]}' for i in self.graph.nodes}

        plt.figure(figsize=(8,6))
        nx.draw(self.graph, pos, with_labels=True, labels=node_labels, node_color='red', node_size=2400, font_color='white' )
        nx.draw_networkx_edge_labels(self.graph,pos=pos, edge_labels=edge_labels)
        plt.show()

    def create_graph(self):
        for i, n in enumerate(self.genome.neuron_genes):
            self.graph.add_node(i, threshold=np.round(n.threshold, 2))
        
        for c in self.genome.connection_genes:
            self.graph.add_edge(c.from_neuron, c.to, weight=np.round(c.weight, 4))
