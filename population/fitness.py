from operator import indexOf
import time
import numpy as np
from agent.Agent import Agent
from sklearn.metrics import log_loss
from scipy.special import expit as sigmoid 
from icecream import ic


"""
This trains the model to store the prev bit only. 
The correct answer is the previous bit
"""
import numpy as np
from sklearn.metrics import log_loss
from scipy.special import expit as sigmoid  # Sigmoid function

def single_memory_bit(agents: list, dataset_size=100, is_testing=False):
    # Generate inputs
    inputs = np.random.randint(2, size=dataset_size)
    inputs[0] = 0
    inputs[1] = 0
    
    for a in agents:
        prev = 0
        prev1 = 1
        predictions = []
        answers = []
        correct = 0
        for i, x in enumerate(inputs):
            val = [1, 0] if x == 0 else [0, 1]
            raw_prediction = a.compute(val)
            prediction = sigmoid(raw_prediction[0])  # Convert to probability
            ans = prev1
            predictions.append(prediction)
            answers.append(ans)
            
            if int(prediction) == ans:
                correct += 1
            if is_testing:
                pred_class = 1 if prediction > 0.5 else 0
                ic(f'Input: {x} answer: {ans} - prediction: {pred_class} ({prediction}) - correct: {correct}')
                
            prev1 = prev
            prev = x

        # Compute BCE loss
        a.score = log_loss(answers, predictions)


def single_input_xor(agents: list[Agent], dataset_size=100, is_testing=False):
    # inputs = np.random.randint(2, size=dataset_size)
    # inputs[0] = 0

    for a in agents:
        inputs = np.random.randint(2, size=dataset_size)
        inputs[0] = 0
        prev = 0
        correct = 0
        for i, x in enumerate(inputs):
            prediction = a.compute([x])[0]
            ic(prediction)
            ans = int(not(prev == x))
            correct += 0 if prediction[0] is not ans else 1
            
            if is_testing:
                ic(f'Input: {x} - prediction: {prediction[0]} - correct: {correct}')
            prev = x
        a.score  = max(correct, 10)

def double_input_xor(agents: list[Agent], dataset_size=100, is_testing=False):
    # inputs = np.random.randint(2, size=dataset_size)
    # inputs[0] = 0

    for a in agents:
        inputs = [tuple(np.random.randint(2, size=2)) for _ in range(dataset_size)]
        correct = 0
        n_same_pred_output = 0
        n_zeros = 0
        n_ones = 0
        prev_pred = 0
        for i, x in enumerate(inputs):
            prediction = a.compute(x)[0]
           
            # prediction = indexOf(prediction, max(prediction))
            if prev_pred == prediction:
                n_same_pred_output += 1
            
            prev_pred = prediction
            ans = x[0] ^ x[1]
            correct += 1 if prediction == ans else 0
            
            n_zeros +=  1 if prediction==0 else 0
            n_ones +=  1 if prediction==1 else 0
            
            
            
            if is_testing:
                ic(f'Input: {x} - ans:{ans} - prediction: {prediction} - correct: {correct}')
                if n_same_pred_output > 80:
                    ic(f'Same prediction count {n_same_pred_output}')
                    correct -= correct*0.05
            
            prev = x
        
        
        if n_same_pred_output > 80:        
            correct -= correct*0.65
        if n_ones - n_zeros < 3:
            correct -= correct*0.31
        a.score  = correct

def negate_bit(agents: list[Agent], dataset_size=100, is_testing=False):
    inputs = np.random.randint(2, size=dataset_size)
    s = time.perf_counter()
    for a in agents:
        correct = 0
        for i, x in enumerate(inputs):
            prediction = a.compute([x])
            correct += 0 if prediction[0] == x else 1
            # correct += 0 if prediction[0] == x else (correct * 0.02) + i
            if is_testing:
                ic(f'Input: {x} - prediction: {prediction[0]} - correct: {correct}')
        a.score = correct
    ic(f'time: {time.perf_counter() - s}')
            
