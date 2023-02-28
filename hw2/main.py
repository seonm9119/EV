import numpy as np
import matplotlib.pyplot as plt
import random


size = 200
crossover_rate = 0.4
mutation_rate = 0.3

def read_data(filename):

    distance = []
    with open(filename, "r") as f:
        body_cnt = 0
        for line in f:
            if body_cnt > 3:
                iwp=line.strip().split()
                tmp= iwp[0].split(',')
                distance.append(list(map(float, tmp)))

            body_cnt+=1
    distance = np.array(distance)

    return distance

def initialize():
    population = []

    for _ in range(100):
        individual = np.arange(0, size)
        np.random.shuffle(individual)
        population.append(individual)

    population = np.array(population)


    return population

def fitness_function(population, distance):
    """Calculate fitness value of an individual."""

    fitness = []


    for pop in population:
        tmp = np.vstack((pop[:size - 1], pop[1:size]))
        sum=0
        for i in range(size - 1):
            idx = tuple(tmp[:, i])
            sum+= distance[idx]
        fitness.append(sum)

    return fitness

def pairwise_tournament(population, fitness):

    pop = population.copy()
    for i in range(100):
        x = random.randint(0, 99)
        if fitness[i] > fitness[x]:
            pop[i] = population[x]

    return pop

def crossover(population):
    np.random.shuffle(population)
    pop, pair = np.array_split(population, 2, axis=0)

    for i in range(50):

        if random.random() < crossover_rate:

            idx = random.sample(range(0, size), 2)
            idx.sort()


            del_idx = []
            for k in pop[i][idx[0]:idx[1] + 1]:
                del_idx.append(np.where(pair[i] == k))

            rearr = pair[i].copy()
            rearr = np.delete(rearr, del_idx)

            l = 0; r = 0
            left_len = idx[0]
            right_len = size - idx[1] - 1

            left = []; right = []
            for k in rearr:
                if l < left_len:
                    left.append(k)
                    l += 1

                    continue

                if r < right_len:
                    right.append(k)

                    r += 1
                    continue

            pair[i] = np.array(left + list(pop[i][idx[0]:idx[1] + 1]) + right)


    population = np.vstack((pop,pair))

    return population

def mutation(population):

    for i in range(100):

        if random.random() < mutation_rate:
            idx = random.sample(range(0, size), 2)
            idx.sort()

            mu = np.flip(population[i][idx[0]:idx[1] + 1])
            population[i][idx[0]:idx[1] + 1] = mu



    return population


def generate(data, figure, save_name):
    """Generate outputs"""

    dist = read_data(data)

    pop = initialize()
    fit = fitness_function(pop, dist)


    avg=[]
    best=[]
    for _ in range(6000):
        pop = pairwise_tournament(pop, fit)
        pop = crossover(pop)
        pop = mutation(pop)
        fit = fitness_function(pop, dist)

        avg.append(np.mean(fit))
        best.append(np.min(fit))



    plt.title("Traveling Salesman Problem fitness trace")
    plt.plot(range(6000), avg, label="Log(Fitness), average")
    plt.plot(range(6000), best, label="Log(Fitness), best")
    plt.legend()
    plt.savefig(figure)
    plt.clf()


    pop=pop.tolist()
    txt = ""
    for i in range(100):
        pop_tmp = "{}".format(pop[i]).lstrip('[').rstrip(']').replace(', ','-')
        txt += pop_tmp + ",{:.6f}\n".format(fit[i])
    with open(save_name, "w") as f:
        f.write(txt)





if __name__ == '__main__':

    for i in range(1,31):
        file_name = "data(TSP)/data-" + str(i) + ".txt"
        save_name = "result/fitness-" + str(i) + ".txt"
        trace_name = "result/trace-" + str(i) + ".png"

        generate(file_name, trace_name, save_name)
        print("Done!")
