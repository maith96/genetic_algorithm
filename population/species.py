import math

import numpy as np
from agent.Agent import Agent
from genes.connection_gene import ConnectionGene
from genes.genome import Genome
from genes.neuron_gene import NeuronGene

from utils import softmax
from icecream import ic
class Species:
    def __init__(self, representative:Agent, alpha=0.5, beta=0.5) -> None:
        self.representative = representative
        self.alpha = alpha
        self.beta = beta
        self.members :list[Agent] = [representative]
        self.best_member = representative
        self.best_score = 0
        self.best_score_in_specie_history = 0
        self.size = 1
    
    def add_member(self, agent:Agent):
        self.members.append(agent)
        self.size = len(self.members)
        
    def same_species(self, other_agent: Agent) -> float:
        similarity = self.alpha * self.get_connection_similarity(self.representative.genome, other_agent.genome) + self.beta * self.get_neuron_functional_diff(self.representative.genome, other_agent.genome)
        return similarity
    

    """
    Calculate the structural difference between two genomes based on their connection genes.
    Args:
        genome1 (Genome): The first genome for comparison.
        genome2 (Genome): The second genome for comparison.
    Returns:
        float: in range(0, 1), which represents structural difference between the two genomes.
        Where 1 means completely different while zero means complete match
    """
    def get_structural_diff(self, genome1:Genome, genome2:Genome) -> float:
        set1 = {(c.from_neuron, c.to) for c in genome1.connection_genes}
        set2 = {(c.from_neuron, c.to) for c in genome2.connection_genes}
        
        conn_unique_to_g1 = [c for c in genome1.connection_genes if (c.from_neuron, c.to) not in set2]
        conn_unique_to_g2 = [c for c in genome2.connection_genes if (c.from_neuron, c.to) not in set1]
        similar_connections = [c for c in genome1.connection_genes if (c.from_neuron, c.to) in set2]
        
        total_unique_connections = len(conn_unique_to_g1) + len(conn_unique_to_g2)
        total_connections = len(genome1.connection_genes) + len(genome2.connection_genes)
        
        if total_connections == 0:
            return 0.0
        
        structural_diff = total_unique_connections / total_connections
        return structural_diff
    
    def get_functional_diff(self, genome1:Genome, genome2:Genome) -> float:
        set1 = {(c.from_neuron, c.to) for c in genome1.connection_genes}
        set2 = {(c.from_neuron, c.to) for c in genome2.connection_genes}
        similar_connections = [c for c in genome1.connection_genes if (c.from_neuron, c.to) in set2]
        
        total_weight_diff = 0.0
        for c1 in similar_connections:
            c2 = list(filter(lambda x: (x.from_neuron, x.to) == (c1.from_neuron, c1.to), genome2.connection_genes))[0]
            weight_diff = abs(c1.weight - c2.weight)
            total_weight_diff += weight_diff
        
        if len(similar_connections) == 0:
            return 0.0
        
        total_unique_connections = len(set1) + len(set2) - (2 * len(similar_connections))
        average_weight_diff = total_weight_diff / len(similar_connections)
        
        functional_diff = average_weight_diff + total_unique_connections
        functional_diff = 0 if functional_diff < 0 else functional_diff
        return functional_diff

    def get_connection_similarity(self, genome1: Genome, genome2: Genome) -> float:
        structural_diff = self.get_structural_diff(genome1, genome2)
        functional_diff = self.get_functional_diff(genome1, genome2)
        if functional_diff < 0:
            ic()
        
        if functional_diff == float('inf'):
            return 0.0
        
        # Normalize structural and functional differences
        normalized_structural_diff = 1.0 / (1.0 + structural_diff)
        normalized_functional_diff = 1.0 / (1.0 + functional_diff)
        
        # Combine the normalized differences to get a similarity score
        similarity = self.alpha * normalized_structural_diff + self.beta * normalized_functional_diff
        
        return similarity
    
    """
    Uses shared connections to find mathing neurons, which are then compared interms of its properties.\n
    What the neuron connects to, or from, is not taken into account.
    """
    def get_neuron_functional_diff(self, genome1: Genome, genome2: Genome):
        matching_conns = self.get_matching_connections(genome1, genome2)
        matched_from_neurons = {(genome1.neuron_genes[c.from_neuron], genome2.neuron_genes[c.from_neuron]) for c in matching_conns}
        matched_to_neurons = {(genome1.neuron_genes[c.to], genome2.neuron_genes[c.to]) for c in matching_conns}
        
        total_from_neurons_similarity_score = sum(self.get_neurons_similarity(g1, g2) for g1,g2 in matched_from_neurons)
        total_to_neurons_similarity_score = sum(self.get_neurons_similarity(g1, g2) for g1,g2 in matched_to_neurons)
        
        total_similarity = total_from_neurons_similarity_score + total_to_neurons_similarity_score
        avg_similarity = total_similarity / ((len(matched_from_neurons) * 2) or 1)
        
        return avg_similarity
        
    """
    returns arange where 1 means similar while 0 means dissimilar completely
    """
    def get_neurons_similarity(self, g1: NeuronGene, g2:NeuronGene) -> float:
        # Calculate the Euclidean distance for numeric attributes
        distance = math.sqrt(
            (g1.resting_potential - g2.resting_potential)**2 
            + (g1.decay_rate - g2.decay_rate)**2
            + (g1.threshold - g2.threshold)**2)
        
        similarity = 1 / (1 + distance)
        return similarity

    
    def get_matching_connections(self, genome1:Genome, genome2:Genome) -> list[ConnectionGene]:        
        set1 = {(c.from_neuron, c.to) for c in genome1.connection_genes}
        set2 = {(c.from_neuron, c.to) for c in genome2.connection_genes}
        matching_connections = [c for c in genome1.connection_genes if (c.from_neuron, c.to) in set2]
        
        return matching_connections
    
    """
    Reproduce, and returns the children
    """
    def procreate(self):
        scores = [a.score for a in self.members]
        scores_to_probabilities = softmax(scores)
        scores_to_probabilities  = [1-s for s in scores_to_probabilities]
        scores_to_probabilities = softmax(scores)

        
        children = []
        for i in range(self.size ):
            if len(self.members) < 2:
                par1 = self.best_member
                par2 = self.best_member
            else:
                par1, par2 = np.random.choice(self.members, 2, p=scores_to_probabilities, replace=False)
            
            if par1.score < par2.score:
                par1.genome.is_dominant = True
                par2.genome.is_dominant = False
            else:
                par1.genome.is_dominant = False
                par2.genome.is_dominant = True
                
            # child = Agent(par1.cross_parents_genome(), par2.cross_parents_genome())
            child = Agent(par1.genome.create_clone(), par2.genome.create_clone())

            children.append(child)
        self.members = []
        return children
    
    def sort_by_score(self):
        self.members = list(sorted(self.members, key=lambda x: x.score, reverse=True))
        self.best_member = self.members[0]
        self.best_score = self.best_member.score
        self.best_score_in_specie_history = self.best_score if self.best_score > self.best_score_in_specie_history else self.best_score_in_specie_history
        self.avg_score = sum(a.score for a in self.members) / len(self.members)
