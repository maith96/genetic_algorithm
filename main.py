from agent.brain_visualizer import BrainVisualizer
from population.fitness import double_input_xor, negate_bit, single_input_xor, single_memory_bit
from population.population import Population
from icecream import ic

population = Population(200, 2, 1)
population.train(double_input_xor, 500, 0.2, True)

# best_agent = population.members[0]
# # visual_brain = BrainVisualizer(best_agent.brain)
# ic(best_agent.compute([0]))
# ic(best_agent.compute([3]))
# visual_brain.draw_graph()