from typing import Self

import numpy as np


class ConnectionGene:
    def __init__(self, _from, _to, _weight):
        self.from_neuron = _from
        self.to = _to
        self.weight = _weight
    
    def create_clone(self) -> Self:
        clone = ConnectionGene(self.from_neuron, self.to, self.weight)
        clone.mutate_weight()
        return clone
    
    def mutate_weight(self):
        will_mutate = np.random.choice([True, False], p=[0.3, 0.7])
        if will_mutate:
            rnd = np.random.ranf()
            if rnd < 0.2:
                self.weight = np.random.uniform(-1, 1)
            else:
                self.weight += np.random.uniform(-1, 1) * self.weight