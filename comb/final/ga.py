#!/usr/bin/env python
# coding: utf-8

import math
from math import sin, pi, exp, log
import random
import matplotlib.pyplot as plt
import numpy as np

import graphs

def survivors(genes, number_keep, fitness_fun):
    fitnesss = [fitness_fun(x) for x in genes]
    genes = [x for _, x in sorted(zip(fitnesss,genes), key=lambda pair: -pair[0])]
    return genes[:number_keep]

def randchance(p):
    return random.random() > p

def mate_to_fill(genes, pop_limit, crossover_fun):
    if pop_limit - len(genes) <= 0:
        raise Exception("woah, slow down there pardner")
    parents = random.sample(genes, (pop_limit-len(genes))*2)
    offspring = []
    for a, b in zip(parents[::2], parents[1::2]):
        offspring.append(crossover_fun(a, b))
    assert(len(genes) + len(offspring) == pop_limit)
    return offspring

def mutate(pop, mutation_fun, mutation_rate):
    return [mutation_fun(x) if randchance(mutation_rate) else x for x in pop]

def one_iteration(pop, fitness_fun, crossover_fun, crossover_rate, 
                  mutation_fun, mutation_rate, niching=None):
    '''
    Crossover rate is the percent of population used to make new offspring.
    Mutation rate is the chance of any new offspring being mutated.
    '''
    size = len(pop)
    num_survive = int(size * (1 - crossover_rate/2))
    
    pop = survivors(pop, num_survive, fitness_fun)
    kids = mate_to_fill(pop, size, crossover_fun)
    kids = mutate(kids, mutation_fun, mutation_rate)
    pop += kids
    return pop

def max_avg_min(ls, fitness_fun):
    ls = [fitness_fun(x) for x in ls]
    return max(ls), sum(ls)/len(ls), min(ls)

def run_graphs(pop_size, mutation_rate, crossover_rate, verbose=False, niching=None):
    pop = [graphs.generate_gene(graphs.size) for _ in range(pop_size)]
    fitness_fun = graphs.fitness
    crossover_fun = graphs.crossover
    mutation_fun = graphs.mutate
    stats = []
    for i in range(10):
        stats.append(max_avg_min(pop, fitness_fun))
        pop = one_iteration(pop, fitness_fun, 
                            crossover_fun, crossover_rate,
                            mutation_fun, mutation_rate, 
                            niching)

    best = max(pop, key=fitness_fun)
    graphs.visualize(best)
    return stats

def plot_stats(stats_list):
    first_time = True
    max_max = -10000

    for stats in stats_list:
        maxx = [x[0] for x in stats]
        avg = [x[1] for x in stats]
        minn = [x[2] for x in stats]
        foo = max(maxx)
        if foo > max_max:
            max_max = foo

        
        if first_time:
            fig, ax1 = plt.subplots()

            ax1.set_xlabel('time (s)')

            def figg(ax, data, color, y_label, alpha):
                ax.set_ylabel(y_label, color=color)
                ax.plot(data, color='tab:' + color, alpha=alpha)
                ax.tick_params(axis='y', labelcolor=color)

            ax2 = ax1.twinx()
            ax3 = ax1.twinx()
            ax3.spines["right"].set_position(("axes", 1.2))
            
            first_time = False

        figg(ax1, minn, 'red', 'min', .3)
        figg(ax2, avg, 'blue', 'avg', .5)
        figg(ax3, maxx, 'green', 'maxx', .8)

    print('max max:', max_max)
    global n_stats
    fig.savefig('stat_' + str(n_stats) + '.png', bbox_inches='tight')
    plt.close(fig)
    n_stats += 1

def random_hillclimbing(start, neighbor_fun, fitness_fun, n_neighbors, n_iterations):
    stats = []
    best = start
    for i in range(n_iterations):
        neighbors = [neighbor_fun(best) for _ in range(n_neighbors)]
        neighbors += [best]
        stats.append(max_avg_min(neighbors, fitness_fun))
        best = max(neighbors, key=fitness_fun)
    graphs.visualize(best)
    print(best)
    return stats

n_stats = 0

for method_or_niching in ['hillclimbing', None]
    stats_list = []
    for i in range(2):
        if method_or_niching == 'hillclimbing':
            stats_list.append(random_hillclimbing(graphs.generate_gene(graphs.size), graphs.neighbor, 
                graphs.fitness, 100, 100))
        else:
            stats_list.append(run_graphs(100, 0.001, 0.2, True, method_or_niching))
    plot_stats(stats_list)


'''
20 0 None m1 20 0
max max: 0.9999999999999993

80 3 sharing m1 80 3
max max: 0.9999999999422162

140 6 crowding m1 140 6
max max: 1.0

40 1 None m4 40 1
max max: 0.9974107140480091

100 4 sharing m4 100 4
max max: 0.9974107121782203

160 7 crowding m4 160 7
max max: 0.9974107140480128

60 2 None m6 60 2
max max: 499.00199538669995

120 5 sharing m6 120 5
max max: 499.0014793607182

180 8 crowding m6 180 8
max max: 499.001996162124
'''
