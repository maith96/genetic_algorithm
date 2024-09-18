import numpy as np
from .brain import Brain
import networkx as nx
import matplotlib.pyplot as plt

from agent import brain


class BrainVisualizer:
    def __init__(self, brain: Brain) -> None:
        self.brain = brain
        self.graph = nx.DiGraph()
        self.create_graph()
    
    def create_graph(self):
        for i, node in enumerate(self.brain.neurons):
            self.graph.add_node(
                i,
                threshold=node.threshold)
            
            connections = []
            for n in self.brain.neurons:
                for c in n.connections:
                    connections.append(c)
            connections = set(connections)
            
            for c in connections:
                self.graph.add_edge(c.from_neuron, c.to_neuron, weight=np.round(c.weight, 4))
                    
    
    def update_graph(self):
        pass
    
    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        node_colors = [self.graph.nodes[i] for i in self.graph.nodes]
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')

        plt.figure(figsize=(8,6))
        nx.draw(self.graph, pos, with_labels=True, node_color='red', node_size=700, font_color='white' )
        nx.draw_networkx_edge_labels(self.graph,pos=pos, edge_labels=edge_labels)
        plt.show()
    

    