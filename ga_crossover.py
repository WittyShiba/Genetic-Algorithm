# crossover.py
'''
Uniform Crossover Algorithm:

Randomly generate a mask = [0,1,0,0,1...0], here 0 = parent 1 and 1 = parent 2.
Loop thru mask:
  if mask element -> parent 1:
    copy parent 1's city to child 1,
    copy parent 2's city to child 2
  if mask element -> parent 2:
    copy parent 2's city to child 1,
    copy parent 1's city to child 2

Also, check for empty args being parsed in to this function.
And check for incorrectly mutated children with duplicate cities.

'''

import numpy as np
import random

def uniform_crossover(parents):
    # calculate number of offsprings we need
    # we divide by 2 because each 2 parents will have 2 kids
    goal = len(parents) // 2     # + (len(parents) % 2 > 0)    # to round up number if division has remainders
    kids = []    # list to hold all children
    count = 0    # counter for number of successful loop

    # check if more than 2 individuals are parsed as parents
    if len(parents) < 2:
      return kids

    # for i in range(goal):    # each loop creates 2 children
    while count <= goal:        
        mask = np.random.randint(0,2, size=8)    # to generate a list of 0s and 1s, as basis for crossover
        two_parents = random.sample(parents, 2)    # select 2 parents randomly from parsed parents
        parent_1, parent_2 = two_parents[0], two_parents[1]    # separate parents into 2 different var
        kid_1, kid_2 = [], []    # place holder for 2 children generated in each iteration
        
        # loop through randomly generated crossover mask
        for i in range(8):
          if mask[i] == 0:
            kid_1.append(parent_1[i])    # copy parent 1's city to child 1
            kid_2.append(parent_2[i])    # parent 2 to child 2
          elif mask[i] == 1:
            kid_2.append(parent_1[i])    # parent 2 to child 1
            kid_1.append(parent_2[i])    # parent 1 to child 2

        # test for duplicate cities in each mutated children
        # each individual should have 8 unique cities, so the unique count should = 8
        unique_cities_1 = len(np.unique(kid_1))
        unique_cities_2 = len(np.unique(kid_2))

        # check for kid 1 duplicate cities
        if unique_cities_1 < 8:
            # print('crossover kid_1 has duplicate cities')
            pass
        elif unique_cities_1 == 8:        
            # write new kid to list of kids
            # print('crossover kid_1 is ok')
            kids.append(kid_1)
            count += 1

        # check for kid 2 duplicate cities
        if unique_cities_2 < 8:
            # print('crossover kid_2 has duplicate cities')
            pass
        elif unique_cities_2 == 8:        
            # write new kid to list of kids
            # print('crossover kid_2 is ok')
            kids.append(kid_2)
            count += 1        
            
    return kids
