import numpy as np
import random

individual_length = 50
population_size = 100
maximum_generation = 300
crossover_rate = 0.02
mutation_rate = 0.8
D = 35


def fitness_function(population):
    """Calculate fitness value of an individual."""

    fitness = []
    for pop in population:
        left, right = np.array_split(pop, 2, axis=0)

        left_u1 = sum(left)
        left_u2 = sum((1-left))

        right_u1 = sum(right)
        right_u2 = sum((1 - right))

        max1 = max(left_u1,left_u2)
        max2 = max(right_u1,right_u2)

        fitness.append(max1+max2)

    fitness = np.array(fitness)

    return fitness

def pairwise_tournament(population, fitness):

    pop = population.copy()
    for i in range(population_size):
        x = random.randint(0, population_size-1)
        if fitness[i] < fitness[x]:
            pop[i] = population[x]

    return pop

def crossover(population):
    """3-points crossover"""

    np.random.shuffle(population)
    pop, pair = np.array_split(population, 2, axis=0)

    for i in range(int(population_size/2)):

        if random.random() <= crossover_rate:
            idx = [0]
            idx += random.sample(range(1, individual_length-1), 3)
            idx.append(individual_length-1)
            idx.sort()

            temp = pop[i].copy()
            for k in range(0, 4, 2):
                pop[i][idx[k]:idx[k + 1]] = pair[i][idx[k]:idx[k + 1]]
                pair[i][idx[k]:idx[k + 1]] = temp[idx[k]:idx[k + 1]]

    population = np.vstack((pop,pair))


    return population

def mutation(population):

    tmp_pop = population.copy()
    for pop in population:
        for i in range(int(individual_length/2)):
            if random.random() < mutation_rate:
                tmp_pop[i] = 1 if pop[i] == 0 else 0

    return tmp_pop

def overlap(population, pre_population, fitness):

    top_portion = 0.15
    split_size = int(top_portion * population_size)
    top_idx = np.flip(fitness.argsort())
    pop_idx = random.sample(range(0, population_size - 1), population_size - split_size)

    pop1 = pre_population[top_idx[0:split_size]]
    pop2 = population[pop_idx]


    new_pop = np.vstack((pop1, pop2))

    return new_pop

def sharing(population, fitness):

    distance = []
    for a in population:
        for b in population:
            distance.append(np.count_nonzero(a!=b))

    distance = np.array(distance, dtype=np.float64).reshape((population_size, population_size))

    distance = np.where(distance >= D, 0, 1-(distance/D))

    eye=1-np.eye(population_size)
    distance = eye*distance

    panelizer = np.sum(distance, axis=0)
    panelizer = np.where(panelizer==0, 1e-6, panelizer)

    fitness = fitness/panelizer

    return fitness



def generate(save_name):
    """Generate outputs"""
    # set seed
    rng = np.random.default_rng(seed=42)
    np.random.seed(42)
    random.seed(42)

    pop = rng.integers(2, size=(population_size,individual_length))
    pre_pop = pop.copy()
    fit = fitness_function(pop)
    fit = sharing(pop, fit)



    for _ in range(maximum_generation):
        pop = pairwise_tournament(pop, fit)
        pop = crossover(pop)
        pop = mutation(pop)

        pop = overlap(pop, pre_pop, fit)
        pre_pop = pop.copy()

        fit = fitness_function(pop)
        fit = sharing(pop, fit)


    text = ""
    for i in range(population_size):
        line = "".join(["1" if b else "0" for b in pop[i]])
        text += line
        text += "\n"


    # output text is always the same
    with open(save_name, "w") as f:
        f.write(text)




if __name__ == '__main__':


    generate("fourmax.txt")
    print("Done!")