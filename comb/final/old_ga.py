#!/usr/bin/env python
# coding: utf-8

import math
from math import sin, pi, exp, log
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def m1(x):
    return sin(5*pi*x)**6
def m4(x):
    return exp(-2 * log(2) * ((x-0.08)/0.854)**2) *               sin(5 * pi * (x**0.75 - 0.5)) ** 6
def a(i):
    return 16 * (i%5 - 2)
def b(i):
    return 16 * (i//5 - 2)
def m6(x, y):
    return 500 - (1 / (.002 + sum([1/(1+i+(x-a(i))**6 + (y-b(i))**6) for i in range(25)])))
m6(10, -2)


# In[4]:



def count_ones(x):
    return sum([int(c) for c in bin(x)[2:]])


# In[5]:


plt.ioff()


# In[6]:


def binprint(x):
    return format(x, "012b")

def new_gene(n_bits):
    return random.randrange(2**n_bits-1)

def uniform_crossover(a, b):
    mask = new_gene(30)
    return (a & mask) | (b & ~mask)

def two_varaible_independant_uniform_crossover(a, b):
    res = []
    for i in [0,1]:
        mask = new_gene(17)
        res.append((a[i] & mask) | (b[i] & ~mask))
    return res

def single_mutation(gene):
    mask = 2**(random.randint(0,30-1))
    return gene ^ mask
def single_mutation_2d(gene):
    masks = [2**(random.randint(0, 17-1)) for _ in range(2)]
    return [gene[i] ^ masks[i] for i in [0,1]]

def to_float(gene):
    return gene/2**30
def to_float2(gene):
    return gene*100/2**17 - 50

def m1_cost(gene):
    return m1(to_float(gene))
def m4_cost(gene):
    return m4(to_float(gene))
def m6_cost(gene):
    return m6(to_float2(gene[0]), to_float2(gene[1]))

def survivors(genes, number_keep, cost_fun):
    costs = [cost_fun(x) for x in genes]
    genes = [x for _, x in sorted(zip(costs,genes), key=lambda pair: -pair[0])]
    return genes[:number_keep]

def hamming_distance(a, b):
    if type(a) is int:
        #return to_float(abs(a-b))
        return count_ones(a^b)
    else:
        #return to_float2(math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2))
        return count_ones(a[0]^b[0]) + count_ones(a[1]^b[1])

def survivors_sharing(genes, number_keep, cost_fun):
    def share(dist):
        delta = 5
        alpha = 2
        if dist < delta:
            return 1 - (dist/delta)**alpha
        else:
            return 0
    costs = []
    for i, gene in enumerate(genes):
        prior_fitness = cost_fun(gene)
        summ = 0
        for j, friend in enumerate(genes):
            if i >= j:
                continue
            summ += share(hamming_distance(gene, friend))
        # avoid division by zero
        if summ == 0:
            summ = .1
        
        costs.append(prior_fitness/summ)
    genes = [x for _, x in sorted(zip(costs,genes), key=lambda pair: -pair[0])]
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

def keep_best(a, b, cost_fun):
    if cost_fun(a) >= cost_fun(b):
        return a
    return b

def deterministic_crowding(pop, crossover_fun, cost_fun, mutation_fun, mutation_rate):
    # crossover rate is not used
    n = len(pop)
    random.shuffle(pop)
    new_pop = []
    for a, b in zip(pop[:n//2], pop[n//2:]):
        # TODO these are independant crossovers, properly they shoud be complimentary
        c1 = crossover_fun(a, b)
        c2 = crossover_fun(a, b)
        
        if randchance(mutation_rate):
            c1 = mutation_fun(c1)
        if randchance(mutation_rate):
            c2 = mutation_fun(c2)
            
        d = hamming_distance
        if d(a, c1) + d(b, c2) <= d(a, c2) + d(b, c1):
            new_pop.append(keep_best(a, c1, cost_fun))
            new_pop.append(keep_best(b, c2, cost_fun))
        else:
            new_pop.append(keep_best(a, c2, cost_fun))
            new_pop.append(keep_best(b, c1, cost_fun))
    return new_pop
    
def mutate(pop, mutation_fun, mutation_rate):
    return [mutation_fun(x) if randchance(mutation_rate) else x for x in pop]

def one_iteration(pop, cost_fun, crossover_fun, crossover_rate, 
                  mutation_fun, mutation_rate, niching=None):
    '''
    Crossover rate is the percent of population used to make new offspring.
    Mutation rate is the chance of any new offspring being mutated.
    '''
    size = len(pop)
    num_survive = int(size * (1 - crossover_rate/2))
    
    if niching == None:
        pop = survivors(pop, num_survive, cost_fun)
        kids = mate_to_fill(pop, size, crossover_fun)
        kids = mutate(kids, mutation_fun, mutation_rate)
        pop += kids
        return pop
    elif niching == 'sharing':
        pop = survivors_sharing(pop, num_survive, cost_fun)
        kids = mate_to_fill(pop, size, crossover_fun)
        kids = mutate(kids, mutation_fun, mutation_rate)
        pop += kids
        return pop
    elif niching == 'crowding':
        pop = deterministic_crowding(pop, crossover_fun, cost_fun, mutation_fun, mutation_rate)
        return pop
    else:
        raise Exception("oops wrong niching")
    assert(len(pop) == size)

def plot_pop_and_landscape(pop, fun, cost_fun):
    fig, ax = plt.subplots()
    ax.set_ylim(ymax = 1.1, ymin = -.1)
    ax.set_xlim(xmax = 1.1, xmin = -.1)
    ax.plot([x/100 for x in range(0,100)], [fun(x/100) for x in range(0,100)], zorder=1)
    ax.scatter([to_float(x) for x in pop], [cost_fun(x) for x in pop], color='red', s=50, zorder=2)
    
    global n_plots
    
    fig.savefig('plot_' + str(n_plots) + '.png', bbox_inches='tight')
    plt.close(fig)
    n_plots += 1
    
def plot_2d_pop_and_landscape(pop, fun, cost_fun):
    fig, ax = plt.subplots()
    z = np.array([[fun(x,y) for x in range(-50, 50)] for y in range(-50, 50)])
    x, y = np.meshgrid(range(z.shape[0]), range(z.shape[1]))
    ax.set_title('z as 2d heat map')
    p = ax.imshow(z,  extent=[-50, 50, -50 , 50])
    fig.colorbar(p)
    ax.scatter([to_float2(x[0]) for x in pop], [to_float2(x[1]) for x in pop])
    
    global n_plots
    fig.savefig('plot_' + str(n_plots) + '.png', bbox_inches='tight')
    plt.close(fig)
    n_plots += 1

    
def max_avg_min(ls, cost_fun):
    ls = [cost_fun(x) for x in ls]
    return max(ls), sum(ls)/len(ls), min(ls)



def run_experiment(pop, cost_fun, fun,
                   crossover_fun, crossover_rate, 
                   mutation_fun, mutation_rate, plot_fun=None, iterations=(5,10),
                   niching=None):
    stats = []
    if plot_fun:
        plot_fun(pop, fun, cost_fun)
    for i in range(iterations[0]):
        for i in range(iterations[1]):
            stats.append(max_avg_min(pop, cost_fun))
            pop = one_iteration(pop, cost_fun, 
                                crossover_fun, crossover_rate,
                                mutation_fun, mutation_rate, 
                                niching)
    if plot_fun:
        plot_fun(pop, fun, cost_fun)
    return stats

def run_m1(pop_size, mutation_rate, crossover_rate, verbose=False, niching=None):
    pop = [new_gene(30) for _ in range(pop_size)]
    fun = m1
    cost_fun = m1_cost
    crossover_fun = uniform_crossover
    mutation_fun = single_mutation
    plot_fun = plot_pop_and_landscape if verbose else None
    return run_experiment(pop, cost_fun, fun,
                          crossover_fun, crossover_rate, 
                          mutation_fun, mutation_rate,
                          plot_fun, (5,40),
                          niching)

def run_m4(pop_size, mutation_rate, crossover_rate, verbose=False, niching=None):
    pop = [new_gene(30) for _ in range(pop_size)]
    fun = m4
    cost_fun = m4_cost
    crossover_fun = uniform_crossover
    mutation_fun = single_mutation
    plot_fun = plot_pop_and_landscape if verbose else None
    return run_experiment(pop, cost_fun, fun,
                          crossover_fun, crossover_rate, 
                          mutation_fun, mutation_rate,
                          plot_fun, (5,40), 
                          niching)

def run_m6(pop_size, mutation_rate, crossover_rate, verbose=False, niching=None):
    pop = [[new_gene(17), new_gene(17)] for _ in range(100)]
    fun = m6
    cost_fun = m6_cost
    crossover_fun = two_varaible_independant_uniform_crossover
    mutation_fun = single_mutation_2d
    plot_fun = plot_2d_pop_and_landscape if verbose else None
    return run_experiment(pop, cost_fun, fun,
                          crossover_fun, crossover_rate, 
                          mutation_fun, mutation_rate,
                          plot_fun, (5, 40),
                          niching)

def plot_stats(stats_list):
    first_time = True
    max_max = -1000000000

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



# Okay so what experiments do I need to run?
# I need to:
# plot fitness vs generation for normal+sharing+crowding
# Do this for all 3 problems
# And repeat each 10 times, keeping best fitness landscape. 
# 
# I also need to vary crossover and mutation rates, I think I'll
# do that for vanilla with all 3 problems, to avoid having a huge amount of
# data.

n_plots = 0
n_stats = 0

plt.ioff()
for niching in [None, 'sharing', 'crowding']:
    for run_fun, name in zip([run_m1, run_m4, run_m6], ['m1', 'm4', 'm6']):
        stats_list = []
        for i in range(10):
            stats_list.append(
                run_fun(100, 0.001, 0.2, True, niching))
        print(n_plots, n_stats, niching, name, n_plots, n_stats)
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
