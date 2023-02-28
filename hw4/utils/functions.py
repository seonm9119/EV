import numpy as np
import random
import math
import sys; sys.setrecursionlimit(10000)
random.seed(42)

def read_data(filename):

    x = []
    y = []
    with open(filename, "r") as f:
        head_cnt=0
        for line in f:
            if head_cnt!=0:
                iwp = line.strip().split()
                tmp = iwp[0].split(',')
                x.append(float(tmp[0]))
                y.append(float(tmp[1]))
            head_cnt+=1

    x = np.asarray(x)
    y = np.asarray(y)

    return x, y

def search(root):
    inv = []

    def preorder(root, depth):
        if root:
            inv.append(root)
            root.depth = depth + 1
            preorder(root.left['address'], root.depth)
            preorder(root.right['address'], root.depth)

    preorder(root, 0)
    return np.asarray(inv)

def clone(root, pop):

    root.root = pop.root
    if pop.left['address']!=None:
        root.left['address'] = Tree(root.depth)
        clone(root.left['address'], pop.left['address'])
    else:
        root.left['value'] = pop.left['value']

    if pop.right['address']!=None:
        root.right['address'] = Tree(root.depth)
        clone(root.right['address'], pop.right['address'])
    else:
        root.right['value'] = pop.right['value']


def convert_formula(tree, constant1=0.2, constant2=0.3):

    cv_operation = {0: '+',
                    1: '-',
                    2: '*',
                    3: '*sin',
                    4: '*cos',
                    5: '*tan'}

    cv_variables = {0: str(constant1),
                    1: str(constant1*10),
                    2: str(constant2),
                    3: str(constant2*10),
                    4: 'x',
                    5: 'x^2',
                    6: 'x^3'}

    txt = []
    def convert(tree):
        txt.append('(')
        if tree.left['value'] == None:
            convert(tree.left['address'])
        else:
            txt.append(cv_variables[tree.left['value']])

        txt.append(cv_operation[tree.root])

        if tree.right['value'] == None:
            convert(tree.right['address'])
        else:
            txt.append(cv_variables[tree.right['value']])
        txt.append(')')

    convert(tree)
    return txt



class Tree():
    def __init__(self,depth):
        self.root = None
        self.right = {'address': None, 'value': None}
        self.left = {'address': None, 'value': None}
        self.depth = depth+1

class Functions():
    def __init__(self, constant1=0.2, constant2=0.3):
        self.operation = {0: lambda x, y: x + y,
                          1: lambda x, y: x - y,
                          2: lambda x, y: x * y,
                          3: lambda x, y: x*math.sin(y),
                          4: lambda x, y: x*math.cos(y),
                          5: lambda x, y: x*math.tan(y) if y!=0 else x*math.tan(0.1)}

        self.variables = {0: lambda x: constant1,
                          1: lambda x: constant1*10,
                          2: lambda x: constant2,
                          3: lambda x: constant2*10,
                          4: lambda x: x,
                          5: lambda x: x ** 2,
                          6: lambda x: x ** 3}


        self.op_size = len(self.operation) - 1
        self.var_size = len(self.variables) - 1


    def create_tree(self,tree, max_depth=2):

        tree.root = random.randint(0, self.op_size)

        if random.random() >= 0.5 and tree.depth <= max_depth:
            tree.left['address'] = Tree(tree.depth)
            self.create_tree(tree.left['address'])
        else:
            tree.left['value'] = random.randint(0, self.var_size)

        if random.random() >= 0.5 and tree.depth <= max_depth:

            tree.right['address'] = Tree(tree.depth)
            self.create_tree(tree.right['address'])
        else:
            tree.right['value'] = random.randint(0, self.var_size)


    def calculate_yhat(self,tree, x):
        def compute(tree):
            left = compute(tree.left['address']) if tree.left['value'] == None else self.variables[tree.left['value']](x)
            right = compute(tree.right['address']) if tree.right['value'] == None else self.variables[tree.right['value']](x)
            return self.operation[tree.root](left, right)

        return compute(tree)

    def pruning(self,population):
        size = population.shape[0]
        idx = random.randint(0, size - 1)

        if random.random() >= 0.5:
            population[idx].left = {'address': None, 'value': random.randint(0, self.var_size)}
        else:
            population[idx].right = {'address': None, 'value': random.randint(0, self.var_size)}

    def modifying(self,population):
        size = population.shape[0]
        idx = random.randint(0, size - 1)
        population[idx].root = random.randint(0, self.op_size)

    def growing(self,population):
        leaf = []
        for pop in population:
            if pop.left['address'] == None:
                dic = {'address': pop, 'direc': 0}
                leaf.append(dic)

            if pop.right['address'] == None:
                dic = {'address': pop, 'direc': 1}
                leaf.append(dic)

        idx = random.randint(0, len(leaf) - 1)

        if leaf[idx]['direc']:
            leaf[idx]['address'].right = {'address': Tree(leaf[idx]['address'].depth), 'value': None}
            self.create_tree(leaf[idx]['address'].right['address'])

        else:
            leaf[idx]['address'].left = {'address': Tree(leaf[idx]['address'].depth), 'value': None}
            self.create_tree(leaf[idx]['address'].left['address'])

