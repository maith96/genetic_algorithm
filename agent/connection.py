from genes.connection_gene import ConnectionGene
from icecream import ic


class Connection:
    def __init__(self, conn: ConnectionGene) -> None:
        self.from_neuron = conn.from_neuron
        self.to_neuron = conn.to
        self.weight = conn.weight
        self.state = 0
    
    def get_state(self):
        s =  self.state
        self.state = 0
        return s
    
    def setState(self, signal):
        self.state = signal * self.weight
        # ic(self.state)
        # ic(signal)