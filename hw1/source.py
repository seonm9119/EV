import matplotlib.pyplot as plt
import random


def read_data(filename):
    """Parse problem specifications from the data file."""
    with open(filename, "r") as f:
        # header
        for line in f:
            iwp = line.strip().split()
            if len(iwp) >= 4 and iwp[2] == "capacity":
                capacity = float(iwp[3])
            elif iwp == ["item_index", "weight", "profit"]:
                table = True
                break
        if not table:
            raise ValueError("table not found.")
        # body
        weights = []
        profits = []
        for line in f:
            i, w, p = line.strip().split()
            weights.append(float(w))
            profits.append(float(p))
    return capacity, weights, profits

def fitness_function(individual, capacity, weights, profits):
    """Calculate fitness value of an individual."""
    sum_weight = 0
    sum_profit = 0
    for bit, weight, profit in zip(individual, weights, profits):
        if bit == "1":
            sum_weight += weight
            sum_profit += profit

    fitness = sum_profit if sum_weight <= capacity else 0
    return fitness

def initialize():
    """Initialize 100 individuals, each of which consists of 10000 bits"""
    population = []
    for _ in range(100):
        individual = ""
        for _ in range(10000):
            individual += "1" if random.random() < 0.5 else "0"
        population.append(individual)
    return population

def generate_example(data, figure, tournament, roulette):
    """Generate example outputs"""
    # generate fitness score trace with some random data
    d1 = [250000 + i * 100 + random.randrange(-800, 800) for i in range(100)]
    d2 = [260000 - (i-100) ** 2 + random.randrange(-800, 800) for i in range(100)]
    plt.title("0/1 Knapsack fitness value trace")
    plt.plot(range(100), d1, label="Pairwise Tournament Selection")
    plt.plot(range(100), d2, label="Roulette Wheel Selection")
    plt.legend()
    plt.savefig(figure)
    plt.show()

    # export two random populations as a txt file
    spec = read_data(data)
    pop1 = initialize()
    pop2 = initialize()

    txt = ""
    for ind1 in pop1:
        fit1 = fitness_function(ind1, *spec)
        txt += "{},{:.6f}\n".format(ind1, fit1)
    with open(tournament, "w") as f:
        f.write(txt)

    txt = ""
    for ind2 in pop2:
        fit2 = fitness_function(ind2, *spec)
        txt += "{},{:.6f}\n".format(ind2, fit2)
    with open(roulette, "w") as f:
        f.write(txt)


if __name__ == '__main__':
    generate_example("Data(0-1Knapsack).txt", "trace.png", "tournament.txt", "roulette.txt")
    print("Done!")
