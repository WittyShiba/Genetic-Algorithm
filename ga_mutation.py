# mutation

'''
Calculate the number of offsprings we need from mutation in this iteration.
Goal is to double the number of parents being parsed in to this function.

Generate 2 random positions for mutation.
Randomly select a parent.
Create a kid by copying that parent.
Mutation happens to the kid at the 2 generated positions.
Gather all correctly mutated kids, and return them when this functions ends.


Also, check for empty args being parsed in to this function.
And check for incorrectly mutated children with duplicate cities.
'''

import numpy as np
import random

def mutation(parents):
    kids = []    # place holder for new offsprings

    # check if parsed parents is empty
    if len(parents) < 1:
        return kids

    # get number of mutated offsprings we need
    goal = len(parents)    # aim to get same number of offsprings and parents; we will double the population subset thru mutation
    count = 0    # to count the number of correctly mutated offsprings
    
    # Do mutation and get correctly mutated offsprings until we reach goal
    while count <= goal:
        # randomly select a parent from the parsed pool of parents
        random_parent = random.choice(parents)
        kid = random_parent    # place holder for mutated kid

        # randomly select 2 positions to swap/shuffle/mutate
        position = np.random.randint(0, 8, size=2)    # range 0-8 to include index 0-7, as each individual has 8 cities

        # mutation happens at the random generated positions
        kid[position[0]], kid[position[1]] = kid[position[1]], kid[position[0]]

        # test for duplicate cities in each individual
        # each individual should have 8 unique cities
        unique_cities = len(np.unique(kid))
        if unique_cities < 8:
            # print('mutation has duplicate cities')
            pass
        elif unique_cities == 8:        
            # write new kid to list of kids
            kids.append(kid)
            count += 1
            # print('mutation is ok')

    return kids
