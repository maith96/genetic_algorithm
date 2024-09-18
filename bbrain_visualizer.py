import matplotlib.pyplot as plt
import networkx as nx
class BBrainVisualizer:
    def __init__(self, brain):
        self.brain = brain
        self.graph = nx.DiGraph()

        self.create_graph()

    def create_graph(self):
        for i, neuron in enumerate(self.brain.neurons):
            self.graph.add_node(i, potential=neuron.potential, threshold=neuron.threshold)

            for conn in neuron.connections:
                target_neuron = conn[0]
                weight = conn[1]
                target_index = self.brain.neurons.index(target_neuron)
                self.graph.add_edge(i, target_index, weight=weight)

    def update_graph(self):
        for i, neuron in enumerate(self.brain.neurons):
            self.graph.nodes[i]['potential'] = neuron.potential

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        node_colors = [self.graph.nodes[i]['potential'] for i in self.graph.nodes]
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')

        plt.figure(figsize=(8, 6))
        nx.draw(self.graph, pos, with_labels=True, node_color=node_colors, node_size=700, cmap=plt.cm.viridis, edge_color='gray', font_color='white')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)

        plt.show()

    def step_and_draw(self):
        self.brain.step()
        self.update_graph()
        self.draw_graph()