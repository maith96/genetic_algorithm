def negate_fitness(brain):
    total_correct = 0

    # Iterate over a set of test inputs
    test_inputs = [0, 1]  # Adjust this set as needed

    for input_value in test_inputs:
        # Set the input value of the brain
        brain.set_input(input_value)

        # Calculate the output of the brain
        output = brain.get_output()

        # Check if the output is the negation of the input
        if output == -input_value:
            total_correct += 1

    # Calculate the fitness as the percentage of correct outputs
    fitness_score = total_correct / len(test_inputs)

    return fitness_score