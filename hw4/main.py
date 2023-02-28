import numpy as np
import random
from utils.functions import *
import matplotlib.pyplot as plt

#제출 결과물과 같은값 출력을 위해 seed설정.


random.seed(42)
population_size=500
max_generation=500
crossover_rate = 0.1
mutation_rate = 0.9



def initialize():

    func = Functions()
    population = []

    for _ in range(population_size):
        root = Tree(0)
        func.create_tree(root)
        inv = search(root)
        population.append(inv)

    population = np.asarray(population)
    return population

def evaluate_fitness(population,x,y):

    fitness = []
    func = Functions()
    for pop in population:
        sum=0
        for i in range(x.shape[0]):
            sum+=(y[i]-func.calculate_yhat(pop[0],x[i]))**2
        fitness.append(sum/x.shape[0])

    return fitness

def pairwise_tournament(population, fitness):

    pop = population.copy()
    for i in range(population_size):
        x = random.randint(0, population_size - 1)
        if fitness[i] > fitness[x]:
            root = Tree(0)
            clone(root, pop[x][0])
            inv = search(root)
            pop[i] = inv

    return pop

def crossover(population):

    #np.random.shuffle(population)
    pop, pair = np.array_split(population, 2, axis=0)

    for i in range(int(population_size/2)):
        if random.random() <= crossover_rate:
            pop_size = pop[i].shape[0]
            pop_idx = random.randint(0, pop_size - 1)

            pair_size = pair[i].shape[0]
            pair_idx = random.randint(0, pair_size - 1)

            rnd = random.random()
            if rnd >=0.5:
                tmp = pop[i][pop_idx].left
                pop[i][pop_idx].left = pair[i][pair_idx].right
                pair[i][pair_idx].right = tmp
            else:
                tmp = pop[i][pop_idx].right
                pop[i][pop_idx].right = pair[i][pair_idx].left
                pair[i][pair_idx].left = tmp

    new_pop = []
    for pop in population:
        inv = search(pop[0])
        new_pop.append(inv)

    return np.asarray(new_pop)

def mutation(population):

    func = Functions()
    functions = {0: lambda x: func.growing(x),
                 1: lambda x: func.pruning(x),
                 2: lambda x: func.modifying(x)}

    for pop in population:
        if random.random() <= mutation_rate:
            choice = random.randint(0, 2)
            functions[choice](pop)

    new_pop = []
    for pop in population:
        inv = search(pop[0])
        new_pop.append(inv)
    return np.asarray(new_pop)

def generate(file_name, save_name, png_name):

    func = Functions()
    x,y = read_data(file_name)

    pop = initialize()
    fit = evaluate_fitness(pop, x,y)


    for _ in range(max_generation):
        pop = pairwise_tournament(pop, fit)
        pop = crossover(pop)
        pop = mutation(pop)
        fit = evaluate_fitness(pop, x,y)
        print("mse : ", np.min(fit))


    idx = np.argmin(fit)
    best_f = pop[idx][0]
    y_hat = []
    for i in range(x.shape[0]):
        y_hat.append(func.calculate_yhat(pop[idx][0], x[i]))


    plt.title("GP-result, Bluedot: data, Orangedot : y_hat")
    plt.scatter(x, y)
    plt.scatter(x, y_hat)
    plt.savefig(png_name)
    plt.clf()

    txt = convert_formula(best_f)

    out = ""
    for t in txt:
        out += t

    print("function : "+out+"\n")
    with open(save_name, "w") as f:
        f.write(out)







if __name__ == '__main__':

    for i in range(1,3):
        print("data-gp" + str(i)+" is running...")
        file_name = "data(gp)/data-gp" + str(i) + ".txt"
        save_name = "result/result-gp" + str(i) + ".txt"
        png_name = "result/result-gp" + str(i) + ".png"
        generate(file_name, save_name, png_name)

    print("Done!")