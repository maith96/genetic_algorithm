import math
import random

class Nneuron:
    def __init__(self, threshold=1.0, resting_potential=0.0, decay=0.1, genes=None):
        if genes is not None:
            self.genes = {
                'threshold': genes['threshold'],
                'resting_potential': genes['resting_potential'],
                'decay': genes['decay'],
                'connections': genes['connections']
            }
        else:
            self.genes = genes
        
        self.threshold = threshold
        self.resting_potential = resting_potential
        self.potential = resting_potential
        self.decay = decay
        self.inputs = []
        self.connections = []

    """
    A method to add a new input to the neuron's list of inputs.
    
    Parameters:
        self (Neuron): The Neuron object.
        weight (float): The weight of the input signal.
        signal (float): The input signal value.
    """
    def add_input(self, weight, signal):
            self.inputs.append((weight, signal))
        
    def process_input(self):
            total_input = sum(weight*signal for weight, signal in self.inputs)
            self.potential += total_input
            self.inputs = []
        
    """
    shifts the neuron's potential towards the resting potential
    """
    def decay_potential(self):
            self.potential = (1 - self.decay) * self.potential + self.decay * self.resting_potential
        
    def fire(self):
        """Determines if the neuron fires based on the threshold."""
        if self.potential >= self.threshold:
            self.potential = self.resting_potential # reset potential after firing
            self.send_signals() # send signals to all connected neurons
            return True
        return False
        
    def step(self) -> bool:
        """A single time step in the neuron's activity."""
        self.process_input()
        
        fired = self.fire()
        self.decay_potential()
        return int(fired)
    
    def connect_to(self, other_neuron, weight):
        """Connects this neuron to another neuron with a specific weight."""
        self.connections.append((other_neuron, weight))
    
    
    def send_signals(self):
        """Sends signals to all connected neurons."""
        for other_neuron, weight in self.connections:
            other_neuron.add_input(weight, 1.0)