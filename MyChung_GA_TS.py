# main TS GA 

"""
#### Data structure ####

- df: Pandas dataframe to hold the csv file, contains distances between cities
- population: list to hold individual routes (pop is a list of list)
  - each route is a list of cities, order matters
- distances: a list of total distance of each individual, for all individuals in population
- fitness_scores: a list of fitness of each individual, for all individuals in population
- mean: a list of the average fitness score of each iteration, for all iterations
- median: a list of median fitness score of each iteration, for all iterations
- std_dev: a list of fitness score standard deviation of each iteration, for all iterations
- global_metrics: list to hold metrics of each iteration, for all iterations
- subset_size: list to hold number of selected individuals at the end of each iteration, for all iterations


#### Algorithm ####

- Read csv file and load to dataframe.
- Generate 50 routes, each route is an individual, all ind's make up the population.
- Calculate metrics for all individuals, aggregate metrics for the first iteration (this iteration).
- Find the individuals performing worse than average fitness score, and delete them.
- Record the remaining individuals.
- Generate new individuals for the next iteration; import 2 .py files as libs.
  - # of new individuals = # of surviving subset from previous iteration
- Start iteration 2, combine all individuals to form new population.
- Calculate metrics.
- Find worst performing individuals, delete, record remaining individuals.
- Generate new individuals via mutation and crossover.
- Check for duplicate cities in mutated children, reject if duplicates are found; only accept "correctly mutated" children.
- Continue for more iterations
...
- Until one individual has reached fitness score of 1.2e^-5 (tentative score, don't know if possible to achieve)
​
​"""

import pandas as pd
import numpy as np
import random
import os

import ga_crossover
import ga_mutation


# Define all functions:

# generate a population with num of individuals
def generate_population(num):    
    population = []    # variable to hold all lists of cities; this is the total population of problem solutions
    for i in range(num):
        global cities    # allow next line to access global var cities; a list a all cities as in csv file
        x = random.sample(cities, k=8)    # randomly shuffle the list without replacement
        population.append(x)
    return population

# take an individual (1 list of cities) and calculate total distance;
# and return a tuple (total_distance, fitness_score)
def metrics(indiv):
    total_dist = 0
    for i in range(8):
        global df
        distance = df[indiv[i]][indiv[i-1]]    # dist = df[city1][city2]
        total_dist += distance
    fitness = 1/total_dist
    return (total_dist, fitness)


# find metrics, surviving individuals, and generate new offsprings; for one iteration
def each_iteration(population):
    # stop this iteration if population size < 1
    new_pop = []
    if len(population) < 1:
        global stop_flag 
        stop_flag = False    # call stop_flag 
        return new_pop    # and exit this iteration
        
    else:
        distances, fitness_scores = [], []    # lists to hold all distances and fitness scores
        for indiv in population:
            dist, fit = metrics(indiv)
            distances.append(dist)
            fitness_scores.append(fit)

        # fitness scores statistics
        fitness_scores = np.array(fitness_scores)
        mean = np.mean(fitness_scores)
        med = np.median(fitness_scores)   
        std_dev = np.std(fitness_scores)
        global global_metrics    # calling global var global_metrics, which is stored in main()
        global_metrics.append([mean, med, std_dev])    # record fitness stats for each iteration

        # individuals with fitness score higher than average will survive, find them
        subset = [(ind,fit) for (ind,fit) in zip(population,fitness_scores) if fit > mean]    # generate list of subset = [(surviving individuals, fitness), (..), ...]
        #print(f'beginning subset: {subset}')
        subset.sort(key=lambda each_sub: each_sub[1], reverse=True)    # reverse sort subset by fitness score
        #print(f'sorted subset: {subset}')
        # delete fitness scores in subset list
        subset = [ind for (ind,fit) in subset] 
        #print(f'final subset: {subset}')

        # stop this iteration if subset is empty
        # for some reason sometimes subset is empty
        if len(subset) < 1:
            return new_pop

    # find and record the best performing individual:
        global best_indiv    # allow next line to access global var best_indiv stored in main()
        candidate_1 = best_indiv              # load previous best individual
        candidate_2 = subset[0]               # subset is reverse sorted, so the subset[0] is the fittest
        cand_1_dist = metrics(candidate_1)    # get total distance of candidate 1
        cand_2_dist = metrics(candidate_2)    # get total distance of cand 2

        if cand_1_dist[0] < cand_2_dist[0]:    # if cand 1 total distance is lower:
            pass    # no change in best individual
        elif cand_2_dist[0] < cand_1_dist[0]:       # if cand 2 total distance is lower:
            best_indiv = candidate_2    # set the new best individual in global variable

    # to record population size and selected subset size
        size_prior = len(population)
        size_posterior = len(subset)
        global pop_size_hist    # calling global var pop_size_hist from main()
        pop_size_hist.append((size_prior, size_posterior))

    # cut surviving individuals, or subset, in half; feed half to uniform corssover and the other half to mutation
        mid_index = len(subset) // 2 
        subset_1 = subset[:mid_index]
        subset_2 = subset[mid_index:]

    # perform uniform crossover on half of the reamining population (subset) to get new offsprings
        children_crossover = ga_crossover.uniform_crossover(subset_1)    # this syntax works, because uniform_crossover() requires 1 arg

    # perform mutation on half of remaining population to get offsprings
        children_mutation = ga_mutation.mutation(subset_2)    # list of new offsprings from mutation

    # pass subset + new offsprings to next iteration
        new_pop = subset

        if children_crossover != None:    # protect against None type being parsed to next iteration
            new_pop.extend(children_crossover)
        
        if children_mutation != None:
            new_pop.extend(children_mutation)

        # new_pop = subset + children_crossover + children_mutation    # this syntax works if None type is never parsed from subsets

        return new_pop


def main():
    # Global variables:
    global population, global_metrics, pop_size_hist, subsets, best_indiv, cities, df
    population = []    # list of individuals, make up for a population
    global_metrics = []    # list to hold (mean,med,std_dev) for all iterations
    pop_size_hist = []     # list to hold beginning and ending population size for all iterations; [(iter1 start size, iter1 end size), ...]
    subsets = []           # list to hold surviving individuals of each iteration, for all iterations
    best_indiv = []        # place holder for the best individual, the 1 and only

    # Load csv file and define some global var, in order to declare functions correctly
    # get dir of this particular GA_TS.py file, whereever it is running
    cwd = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(cwd, 'TS_Distances_Between_Cities.csv')    # complete dir by adding target csv file

    df = pd.read_csv(file_path, index_col=0)    # load csv file
    df = df.drop([np.NaN])    # drop last row, all NaN values;  do not use inplace=True
    cities = list(df.columns)    # a list of all city names; global var

    # randomly generate 50 non-repeating samples, and form a population
    population = generate_population(50)

    # manually/randomly pick an individual as best individual, so that iteration 1 has a starting point for this variable
    # IMPORTANT to use [0], because random.sample returns a list of list here.
    best_indiv = random.sample(population, 1)[0]

    # set stopping criteria for iterations
    flag_fitness = True    # stop the iterations if 1 individual reaches target fitness
    stop_flag = True    # functions can change this flag to stop the loop
    count = 0    # stop the iteration if it has iterated 100 times
    target_fitness = 0.00030    # arbitary target fitness is 3e^-5, or 0.00003

    # start iterations until one of the conditions are satisfied
    while flag_fitness and stop_flag and count < 50:
        # break while loop if population < 2
        if len(population) < 1:    
            break
        else:
            # carry out all actions in each iteration
            population = each_iteration(population)

            # adjust stopping criteria
            count += 1
            best_ind_metrics = metrics(best_indiv)    # calculate metrics of best individual of this iteration
            if best_ind_metrics[1] >= target_fitness:    # if the new best individual has fitness score higher than target, then stop the iterations
                flag_fitness = False

    # create Results.txt file
    result = []    # place holder for words to write to txt file
    # get each city from the best individual
    for index, city in enumerate(best_indiv):
        result.append(f'{index + 1} / {city}' + '\n')
    # get total distance of the best individual
    best_dist = metrics(best_indiv)
    result.append(f'Total distance of best individual: {best_dist[0]}')
    # create and write to txt file
    result_file_path = os.path.join(cwd, 'MyChung_GA_TS_Result.txt')    # find current dir and name the txt file
    with open(result_file_path, 'w') as f:
        for ele in result:
            f.writelines(ele)

    # create Info.txt file
    info = []    # place holder for lines to write to txt file
    for i in range(len(pop_size_hist)):    # loop thru all iterations and find metrics
        info.append(f'{i+1}. Population size: {pop_size_hist[i][0]} for iteration {i+1}' + '\n' +
                f'   Average fitness score: {global_metrics[i][0]}' + '\n' +
                f'   Median fitness score: {global_metrics[i][1]}' + '\n' +
                f'   STD of fitness scores: {global_metrics[i][2]}' + '\n' +
                f'   Size of the selected subset of population: {pop_size_hist[i][1]}' + '\n' + '\n')
    info_file_path = os.path.join(cwd, 'MyChung_GA_TS_Info.txt')    # find current dir and name the txt file
    with open(info_file_path, 'w') as f:
        for ele in info:
            f.writelines(ele)


# call main function
if __name__ == '__main__':
    main()
