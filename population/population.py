import numpy as np
from agent.Agent import Agent
from genes.connection_gene import ConnectionGene
from genes.genome import Genome
from genes.neuron_gene import NeuronGene

from icecream import ic

from genes.visualize_genome import VisualizeGenome
from population.species import Species
from utils import softmax

class Population:
    def __init__(self, size, num_inputs, num_outputs) -> None:
        self.size = size
        self.num_inputs = num_inputs
        self.num_outputs = num_outputs
        
        self.members = self.create_first_generation()
        self.species:list[Species] = list()
        self.highest_score = 0
        
        self.group_into_species()
        
    def create_first_generation(self) -> list[Agent]:
        members: list[Agent] = list()
        
        for i in range(self.size):
            neurons: list[NeuronGene] = list()
            # create input neurons
            neurons += [NeuronGene() for _ in range(self.num_inputs)]
            # create output
            neurons += [
                NeuronGene(
                np.random.uniform(-3, 3),
                np.random.uniform(-3, 3),
                np.random.uniform(-3, 3),
                np.random.ranf(),
                'output',
                ) for _ in range(self.num_outputs)
                ]
                        
            par1_g = Genome([], neurons)
            for i in range(max(self.num_outputs**self.num_inputs, 6)):
                #create connections between input and output
                par1_g.mutate_new_connection()
                
            par2_g = par1_g.create_clone()
            
            members.append(Agent(par1_g, par2_g))
        
        return members
    
    def procreate(self):
        self.change_species_size()
        children = []
        for s in self.species:
            children += s.procreate()
            
        self.members = children
    
    def train(self, fitness, generations, illicitism = 0.2, testing=False):
        for i in range(1, generations):
            fitness(self.members)
            # self.members = list(sorted(self.members, key=lambda x: x.score, reverse=True))
            self.group_into_species()
            self.sort_species()
            
            # n_survivors = illicitism * len(self.members)
            # survivors = self.members[:int(n_survivors)]
          
            best_score = self.species[0].best_score
            if best_score > self.highest_score:
                b = self.species[0].best_member
                # b.visualize()
                v = VisualizeGenome(b.genome)
            if best_score > self.highest_score and testing:
                self.test_the_best(fitness)
            
            self.highest_score = best_score if best_score > self.highest_score else self.highest_score
            
            ic(f'Generation: {i}')
            ic(f'Highest Score: {(self.highest_score)}')
            ic(f'Best Score: {(self.species[0].best_score)}')
            ic(f'Worst Score: {(self.species[-1].members[-1].score)}')
            ic(f'Number of species: {len(self.species)}\n')
            
            self.procreate()
    
    def test_the_best(self, fitness):
        best_agent = self.species[0].best_member
        fitness([best_agent], is_testing=True)
    
    def group_into_species(self) -> None:
        self.species = []
        for a in self.members:
            found_specie = False
            
            for specie in self.species:
                similarity = specie.same_species(a)
                if  similarity > 0.1:
                    specie.add_member(a)
                    found_specie = True
                    break
            if not found_specie:
                self.species.append(Species(a))
        self.species = list(filter(lambda x: len(x.members) > 0, self.species))
        
        # for i,s in enumerate(self.species):
        #     ic(f'specie {i+1}: {s.size}')
        # ic(f'Total Number of individuals: {sum(s.size for s in self.species)}')

    def sort_species(self):
        for s in self.species:
            s.sort_by_score()
        self.species = list(sorted(self.species, key=lambda x: x.best_score, reverse=True))
    
    def change_species_size(self):
        self.species = list(sorted(self.species, key=lambda x: x.avg_score, reverse=True))
        scores = [a.avg_score for a in self.species]
        probabilities = softmax(scores)
        probabilities = list(map(lambda x: round(x,1), probabilities))
        # self.species[0].size += 1
        # self.species[-1].size -= 1
        # for s, p in zip(sorted_by_avg_Score, probabilities):
        #     new_size = p*self.size
        #     s.size = max(int(), 1)
        ic(f'Total Number of individuals: {sum(s.size for s in self.species)}')

            