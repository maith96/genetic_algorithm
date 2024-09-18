import random

from vbrain import Brain

class Population:
    def __init__(self, size, genetic_structure):
        self.size = size
        self.individuals = []
        self.genetic_structure = genetic_structure

        self.create_population()

    def create_population(self):
        for _ in range(self.size):
            # Create a random genetic structure for the last neuron in each gene

            individual = Brain(
                [
                    # input neuron
                    {
                      'threshold': 1.0,
                      'resting_potential': 0.0,
                      'decay': 0.1,
                      'connections': [(2, 1.0)]
                    },
                    # output neuron
                    {
                      'threshold': 1.0,
                      'resting_potential': 0.0,
                      'decay': 0.1,
                      'connections': []
                    },
                    
                    # Hidden neurons
                    {
                    'threshold': random.uniform(-5, 5),
                    'resting_potential': random.uniform(-5, 5),
                    'decay': random.uniform(0, 1),
                    'connections': [(1, random.uniform(-1, 1))]
                }]
                )
            self.individuals.append(individual)


    def get_fittest(self):
        # Implement your fitness function here
        pass

    def crossover(self, parent1, parent2):
        # choose a random crossover point
        crossover_point = random.randint(1, len(parent1.genetic_structure)-1)
        
        # combine the parts from both parents
        child_genetic_structure = parent1.genetic_structure[:crossover_point] + parent2.genetic_structure[crossover_point:]
        child = Brain(child_genetic_structure)
        
        return child

    def mutate(brain):
        # Choose a random neuron to mutate
        neuron_index = random.randint(0, len(brain.genetic_structure) - 1)
    
        # Get the current neuron
        neuron = brain.genetic_structure[neuron_index]
    
        # Choose a random attribute to mutate
        attribute = random.choice(['threshold', 'resting_potential', 'decay'])
    
        # Mutate the attribute by adding a random value within a certain range
        mutation_range = (0.1, 0.5)  # Adjust this range as needed
        mutation_value = random.uniform(*mutation_range)
        neuron[attribute] += mutation_value
    
        return brain