import numpy as np
from agent.brain import Brain
from genes.connection_gene import ConnectionGene
from genes.genome import Genome
from genes.neuron_gene import NeuronGene

from icecream import ic

from genes.visualize_genome import VisualizeGenome
from utils.crossover import cross_genomes
class Agent:
    def __init__(self, par1_genome: Genome, par2_genome:Genome) -> None:
        self.score = 0.0
        self.par1_genome = par1_genome
        self.par2_genome = par2_genome
        self.genome = self.cross_parents_genome()
        # ic(f"connections: {len(self.genome.connection_genes)}")
        
        self.brain = Brain(self.genome.connection_genes, self.genome.neuron_genes)
    
    def compute(self, inputs: list):
        # if len(self.genome.neuron_genes) > 2:
        #     if self.genome.connection_genes[-1].from_neuron != 0:
        #         self.visualize()
        #         ic()
        return self.brain.simulate(inputs)
    
    """
    Creates a new Genome by crossing parents matching genes(genomes). Sort of like Miosis.\n
    This method is used to create a gamete that wil be crosed with another gamete, and determine the traits/genes of current Agent 
    """
    def cross_parents_genome(self)->Genome:
        if self.par1_genome.is_dominant:
            return cross_genomes(self.par1_genome,self.par2_genome)
        else:
            return cross_genomes(self.par2_genome,self.par1_genome)
        # par1_clone = self.par1_genome.create_clone()
        # par1_clone.is_dominant = self.par1_genome.is_dominant
        # par2_clone = self.par2_genome.create_clone()
        # par2_clone.is_dominant = par2_clone.is_dominant
        
        # crossed_connection_genes, excessive_connection_genes = self.cross_conn_genes(par1_clone.connection_genes, par2_clone.connection_genes, par1_clone, par2_clone)
        # complete_connection_genes = crossed_connection_genes + excessive_connection_genes
        # crossed_neuron_genes = self.cross_neuron_genes(crossed_connection_genes, par1_clone, par2_clone)
        
        # return Genome(complete_connection_genes, crossed_neuron_genes)
    
    def visualize(self):
        visual = VisualizeGenome(self.genome)