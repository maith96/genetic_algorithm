from vbrain import Brain
from bbrain_visualizer import BrainVisualizer
from nnnnnnnneuron import Neuron

genetic_structure = [
    # Input neuron
    {
        'threshold': 1.0,
        'resting_potential': 0.0,
        'decay': 0.1,
        'connections': [(1, 1.0)]
    },
    
    # Hidden neurons
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
    }
]

brain = Brain(genetic_structure)
brain_visualizer = BrainVisualizer(brain)


for _ in range(10):
    print(brain.step())
    

brain_visualizer.step_and_draw()