
from typing import overload, override

import numpy as np
from agent.connection import Connection
from genes.connection_gene import ConnectionGene
from icecream import ic


class Neuron:
    def __init__(self, threshold=1.0, resting_potential=0.0, starting_potential=0.0, decay=0.9, neuron_type='input'):
        self.neuron_type = neuron_type
        self.threshold = threshold
        self.resting_potential = resting_potential
        self.current_potential = starting_potential
        self.decay = np.round(decay, 2)
        self.inputs = []
        
        self.connections: list[Connection] = list()
        self.synapes: list[Connection] = list()
        self.dendrites: list[Connection] = list()
        
        if self.resting_potential >= self.threshold:
            self.resting_potential = self.threshold *0.3
        
        self.max_potential = self.resting_potential * 1.5
        self.min_potential = self.resting_potential * 0.3
    
        self.is_exhausted = False
        
    def connect_to(self, connection: Connection):
        """Connects this neuron to another neuron with a specific weight."""
        self.connections.append(connection)
    
    def connect_synapse(self, connection: Connection):
        self.synapes.append(connection)
    
    def connect_dendrite(self, connection: Connection):
        self.dendrites.append(connection)
    
    """
    Simulates the activity of this individual neuron
    if x is provided then its an input neuron
    """
    def simulate(self, x=None):
        # check if this is an input neuron   
        if x is not None:
            self.current_potential += x
        
        self.current_potential += self.get_sum_of_inputs()
        isTriggered = (self.current_potential - self.threshold) >= 0
            
        if isTriggered: 
            self.propagate_potential(self.current_potential * self.decay)
            self.decay_potential()
            
            # if self.neuron_type == 'output':
            #     return self.current_potential
            return 1
        else: 
            self.decay_potential()
            # if self.neuron_type == 'output':
            #     return self.current_potential
            return 0
    
    
    def get_sum_of_inputs(self):
        return sum(s.get_state() for s in self.synapes)
    
    def propagate_potential(self, signal):
        for d in self.dendrites:
            d.setState(signal)
    
    def get_data(self):
        return {
        'neuron_type': self.neuron_type,
        'threshold': self.threshold,
        'resting_potential': self.resting_potential,
        'current_potential': self.current_potential,
        'decay': self.decay,
        'synapses_activity': self.get_synapses_activity()
    }
    
    
    def decay_potential(self):
        # self.current_potential = (1 - self.decay) * self.current_potential + self.decay * self.resting_potential
        self.current_potential = np.round(self.current_potential, 2)
        # self.current_potential = self.threshold
        self.current_potential = self.current_potential * self.decay