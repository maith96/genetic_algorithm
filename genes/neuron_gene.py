from typing import Self

import numpy as np


class NeuronGene:
    def __init__(self, threshold=1.0, resting_potential=0.0, starting_potential=0.0, decay=1, neuron_type='input'):
        self.resting_potential = resting_potential
        self.decay_rate = decay
        self.threshold = threshold
        self.neuron_type = neuron_type
        self.starting_potential = starting_potential
        
        if neuron_type != 'input':
            self.max_potential = self.resting_potential * 3
            self.min_potential = self.resting_potential * -3
    
    def create_clone(self) -> Self:
        clone = NeuronGene(self.threshold, self.resting_potential,self.starting_potential , self.decay_rate, self.neuron_type)
        clone.mutate()
        return clone
        
    def mutate(self):
        will_mutate = np.random.choice([True, False], p=[0.3, 0.7])
        if will_mutate:
            rnd = np.random.ranf()
            
            if rnd < 0.1:
                self.mutate_threshold()
            elif rnd < 0.6:
                self.mutate_resting_potential()
            elif rnd < 0.9:
                self.mutate_decay_rate()
            else:
                self.mutate_starting_potential()



    def mutate_threshold(self):
        self.threshold = self.mutate_variable(self.threshold)
            
    def mutate_resting_potential(self):
        self.resting_potential = self.mutate_variable(self.resting_potential)
            
    def mutate_decay_rate(self):
        self.decay_rate = self.mutate_variable(self.decay_rate)
    
    def mutate_starting_potential(self):
        self.decay_rate = self.mutate_variable(self.starting_potential)
    
    def mutate_variable(self, variable):
        rnd = np.random.ranf()
        if rnd < 0.05:
            return np.random.uniform(-1, 1)
        else:
            return (variable + np.random.uniform(-1, 1) * variable)
    