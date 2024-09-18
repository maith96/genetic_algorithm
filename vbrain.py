from nnnnnnnneuron import Neuron


class Brain:

    def __init__(self, genetic_structure):
        self.neurons = []
        self.genetic_structure = genetic_structure
        self.create_neurons_from_genetic_structure(genetic_structure)
        self.connect_neurons_from_genetic_structure(genetic_structure)
        
    
    def create_neurons_from_genetic_structure(self, genetic_structure):
        for gene in genetic_structure:
            neuron = Neuron(threshold=gene['threshold'], resting_potential=gene['resting_potential'], decay=gene['decay'])
            self.neurons.append(neuron)
    
    def connect_neurons_from_genetic_structure(self, genetic_structure):
        for i, gene in enumerate(genetic_structure):
            for connection in gene['connections']:
                target_neuron_idx, weight = connection
                self.neurons[i].connect_to(self.neurons[target_neuron_idx], weight)
    
    def step(self):
        # self.neurons[0].add_input(1.5, 1.0)
        output = False
        for neuron in self.neurons:
            output = neuron.step()
        
        return output