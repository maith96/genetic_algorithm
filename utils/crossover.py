import numpy as np

from genes.connection_gene import ConnectionGene
from genes.genome import Genome
from genes.neuron_gene import NeuronGene
from icecream import ic
"""
    Crosses two genomes to generate a new genome.
    
    Args:
        par1_genome (Genome): The dominant parent genome to cross.
        par2_genome (Genome): The recessive parent genome to cross.
        
    Returns:
        Genome: The newly generated genome after crossing the input parent genomes.
"""
def cross_genomes(par1_genome: Genome, par2_genome: Genome) -> Genome:
    crossed_connections, unique_to_dominant_connections = cross_connections(par1_genome.connection_genes, par2_genome.connection_genes)
    crossed_neuron_genes = cross_neuron_genes(crossed_connections, par1_genome, par2_genome)
    connections = crossed_connections + unique_to_dominant_connections
    
    return Genome(connections, crossed_neuron_genes)


"""
    Crosses the connection genes from two lists to generate a new list of connection genes.
    Args:
        conn_genes1 (list[ConnectionGene]): The connection genes from the dominant parent genome.
        conn_genes2 (list[ConnectionGene]): The connection genes from the recessive parent genome.
    Returns:
        list[ConnectionGene]: A tuple containing the crossed matching connections and unique connections of the dominant parent.
"""
def cross_connections(conn_genes1: list[ConnectionGene], conn_genes2: list[ConnectionGene]) -> list[list[ConnectionGene], list[ConnectionGene]]:
    set1 = {(c.from_neuron, c.to) for c in conn_genes1}
    set2 = {(c.from_neuron, c.to) for c in conn_genes2}
    
    matching_sets = set1 & set2
    unique_to_dominant = set1 - matching_sets
    
    domminant_matching_connections: list[ConnectionGene] = [next((c for c in conn_genes1 if (c.from_neuron, c.to) == s), None) for s in matching_sets]
   
    recessive_matching_connections: list[ConnectionGene] = [next((c for c in conn_genes2 if (c.from_neuron, c.to) == s)) for s in matching_sets]
    
    
    crossed_matching_connections = []
    for c1, c2 in zip(domminant_matching_connections, recessive_matching_connections):
        if c1.from_neuron != c2.from_neuron or c1.to != c2.to:
            ic()
        chosen = np.random.choice((c1, c2), p=[0.5, 0.5])
        crossed_matching_connections.append(chosen.create_clone())
    
    unique_to_dominant_connections = [c.create_clone() for c in conn_genes1 if (c.from_neuron, c.to) in unique_to_dominant]
    complete_new_connections = crossed_matching_connections + unique_to_dominant_connections
    
    return (crossed_matching_connections, unique_to_dominant_connections)


def cross_neuron_genes(crosed_connection_genes: list[ConnectionGene], par1_genome:Genome, par2_genome:Genome) -> list[NeuronGene]:    
    all_neuron_indices_in_shared_connections = [c.from_neuron for c in crosed_connection_genes] + [c.to for c in crosed_connection_genes]
    unique_neuron_indices = {i for i in all_neuron_indices_in_shared_connections}
    # if len(crosed_connection_genes) > 1:
    #     ic()
    
    crossed_neuron_genes = [n.create_clone() for n in par1_genome.neuron_genes]
    
    for i in unique_neuron_indices:
        chosen = np.random.choice([par1_genome.neuron_genes[i], par2_genome.neuron_genes[i]], p=(0.6, 0.4))
        crossed_neuron_genes[i] = chosen.create_clone()
    
    return crossed_neuron_genes