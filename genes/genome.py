from genes.connection_gene import ConnectionGene
from genes.neuron_gene import NeuronGene

from typing import Self

import numpy as np
from icecream import ic

class Genome:
    def __init__(self, 
                 connection_genes: list[ConnectionGene], 
                 neuron_genes: list[NeuronGene]
                 ) -> None:
        self.connection_genes: list[ConnectionGene] = connection_genes        
        self.neuron_genes: list[NeuronGene] = neuron_genes
        
        self.is_dominant = False
    
    """
    Performs crossover between this genome and another.
    This current genome will be the dominant one over the other genome.
    Clones of the parents are created first and then the crossover is performed.
    """
        
    def create_clone(self, mutation_rate=0.05) -> Self:
        connections = [gene.create_clone() for gene in self.connection_genes]
        neurons = [gene.create_clone() for gene in self.neuron_genes]
        clone = Genome(connections, neurons)
        clone.is_dominant = self.is_dominant
        
        if np.random.ranf() < mutation_rate:
            clone.mutate()

        return clone
    
    def mutate(self):
        rnd = np.random.ranf()
        if rnd < 0.4:
            if len(self.neuron_genes) < 7:
                self.mutate_new_neuron()
            return
        elif rnd < 0.8:
            self.mutate_new_connection()
        # ic(len(self.connection_genes))
    
    def  add_connection(self, connection:ConnectionGene) -> None:
        self.connection_genes.append(connection)
    
    def remove_connection(self, connection:ConnectionGene) -> None:
        self.connection_genes.remove(connection)
    
    def mutate_new_connection(self, to=None) -> ConnectionGene:
        from_neuron = np.random.randint( (len(self.neuron_genes)))
        to_neuron = to if to else np.random.randint( (len(self.neuron_genes)))
        weight = np.random.uniform(-1, 1)
        new_conn = ConnectionGene(from_neuron, to_neuron, weight)
        
        conn_exists = False
        for i in range(10):
            for c in self.connection_genes:
                if c.from_neuron == new_conn.from_neuron and c.to == new_conn.to:
                    conn_exists = True
                    break
            if conn_exists:
                new_conn = ConnectionGene(from_neuron, to_neuron, weight)
            else:
                self.add_connection(new_conn)
        
        return None
    
    """
    Breaks an existing connection and adds a new Neuron between them with random values for its attributes.
    
    Returns:
        Genome: A modified genome with the new connections and neuron.
    """
    def mutate_new_neuron(self) -> None:
        connections = self.connection_genes
        random_connection_gene = connections[np.random.randint(0, len(connections))]
        
        new_neuron_gene = NeuronGene(
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1),
                np.random.uniform(-1, 1),
                np.random.uniform(0, 1.4),
                'internal',
                )
        
        self.neuron_genes.append(new_neuron_gene)
        new_neuron_idx = len(self.neuron_genes) -1
        
        new_conn1 = ConnectionGene(random_connection_gene.from_neuron, new_neuron_idx, random_connection_gene.weight / 2)
        new_conn2 = ConnectionGene(new_neuron_idx, random_connection_gene.to, np.random.uniform(-1,1))
        
        connections.remove(random_connection_gene)
        
        connections.append(new_conn1)
        connections.append(new_conn2)