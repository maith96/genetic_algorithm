from typing import Self
from agent.connection import Connection
from genes.connection_gene import ConnectionGene
from genes.neuron_gene import NeuronGene

from agent.neuron import Neuron

from icecream import ic

class Brain:
    """
    Create a Brain from genes
    """
    def __init__(self, connection_genes, neuron_genes: list[NeuronGene]):
        self.create_neurons(neuron_genes)
        self.create_connections(connection_genes)
        self.add_connections_to_neurons(connection_genes)
        
        self.input_neurons: list[Neuron] = self.get_input_neurons()
        self.internal_neurons: list[Neuron] = self.get_internal_neurons()
        self.output_neurons: list[Neuron] = self.get_output_neurons()
    
    def create_neurons(self, neuron_genes: list[NeuronGene]):
        self.neurons: list[Neuron]  = list(
            [Neuron(
                gene.threshold, 
                gene.resting_potential, 
                gene.starting_potential,
                gene.decay_rate,
                gene.neuron_type)
             for gene in neuron_genes]
            )
    
    def add_connections_to_neurons(self, connection_genes: list[ConnectionGene]):
        for conn in self.connections:
            from_neuron = self.neurons[conn.from_neuron]
            to_neuron = self.neurons[conn.to_neuron]
            
            to_neuron.connect_synapse(conn)
            from_neuron.connect_dendrite(conn)
            
    
    def create_connections(self, connection_genes: list[ConnectionGene]):
        self.connections = [Connection(gene) for gene in connection_genes]
        
    """
    Simulates the entire brain activity. Takes in x as inputs and feeds it to input neurons"""
    def simulate(self, x):
        # if len(self.internal_neurons) > 0:
        #     ic()
        self.simulate_input_neurons(x)
        self.simulate_internal_neurons()
        outputs = self.simulate_output_neurons()
        
        return outputs
    
    def simulate_input_neurons(self, inputs:list):
        # ic()
        for x, n in zip(inputs, self.input_neurons):
            n.simulate(x)
            # ic(n.get_data())
    
    def simulate_internal_neurons(self):
        # ic()
        for n in self.internal_neurons:
            n.simulate()
            # ic(n.get_data())
        
    def simulate_output_neurons(self) -> list:
        # ic()
        outputs = []
        # ic(len(self.output_neurons))
        for n in self.output_neurons:
            outputs.append(n.simulate())
            # ic(n.get_data())
        return outputs
            
    
    def get_input_neurons(self) -> list:
        return list(filter(lambda x: x.neuron_type == 'input', self.neurons))
        
    def get_internal_neurons(self) -> list:
        return list(filter(lambda x: x.neuron_type == 'internal', self.neurons))
        
    def get_output_neurons(self) -> list:
        return list(filter(lambda x: x.neuron_type == 'output', self.neurons))
    