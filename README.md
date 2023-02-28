## GIST Evolutionary AI 2021 Fall Homework


### Homework 1 - Knapsack Problem

Solve 0/1 Knapsack Problem using two kinds of GA:
- Roulette wheel selection, 3-point crossover, and bitwise mutation.
- Pairwise tournament selection, 3-point crossover, and bitwise mutation.

### Homework 2 - Traveling Salesman Problem

Traveling salesman problem is to find a route that visits all cities in a minimum travel distance. Solve 30 Traveling Salesman Problems using Genetic Algorithm.
The problem specifications are in data (TSP). Each text file (data 1.txt, data
2.txt, … data-30.txt) has a table that represents the distance between cities. The travel distance of a route is the sum of the distance of the adjacent cities. For example, 3-0-1-2 has a travel distance of table[3][0] + table[0][1] + table[1][2].

### Homework 3 - FourMax Problem

The TwoMax problem is a multimodal optimization problem that has 2 optimal solutions. The fitness function of the TwoMax problem is:

$$f(x)=max\left ( u(x), \bar{u}(x) \right )$$
$$u(x)=\sum_{i=1}^{n}x_{i}$$
$$\bar{u}(x)=\sum_{i=1}^{n}(1-x_{i})$$
where $x=\left< x_{1}, x_{}, ..., x_{n} \right>$ ,      $x_{i}\in$ {0,1}.

In this homework assignment, we introduce the FourMax problem. FourMax problem has 4 optimal solutions, and one FourMax problem is made by concatenating two TwoMax problems.

### Homework 4 - Genetic Programming

Use genetic programming to find the symbolic formula (f) that most accurately describes the given data. Each data (data gp1.txt, data gp2.txt) contains 200 xy coordinates, where
$$y=f(x) + noisy$$
