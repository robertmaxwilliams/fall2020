import numpy as np
import math
import scipy
from scipy.sparse.csgraph import shortest_path
import random
import json

import visualizer

def randp():
    return random.randrange(2) == 0

points = [[0.2, -1.4],
          [1.1, 0.9],
          [1.9, -1.5],
          [3.1, 2.3]]
points = []
cities = json.load(open('cities.json'))
for city in cities[:10]:
    points.append((city['latitude'], city['longitude']))


size = len(points)




def dist(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def make_distance_matrix(points):
    n = len(points)
    mat = np.zeros((n,n))
    for i, a in enumerate(points):
        for j, b in enumerate(points):
            mat[i,j] = dist(a,b)
    return mat

dists = make_distance_matrix(points)

def normalize_gene(gene, total=1.0):
    ''' set spending on lower diagonal and on
    diagonal to zero and force it to sum
    to 1 (or total, if supplied'''
    # replace negatice withe zero
    gene[gene<0] = 0
    gene = np.triu(gene)
    np.fill_diagonal(gene, 0)
    return total*gene/np.sum(gene)

def generate_gene(size):
    gene = np.random.rand(size, size)
    return normalize_gene(gene)

def gene_to_distance_matrix(gene, dmat):
    '''The gene has the amount spent on each 
    edge, from 0 to 1. These are interpreted as the speed that
    you can travel on that road. The result is how long it takes
    to travel each edge, given the gene's investment in each edge.'''
    with np.errstate(divide='ignore', invalid='ignore'):
        travel_times = dmat/gene
    np.fill_diagonal(travel_times, 0)
    return travel_times

def sum_shortest_paths(gene):
    times = gene_to_distance_matrix(gene, dists)
    sp = shortest_path(times, directed=False)
    return np.sum(sp)

def remove_edge(graph, e):
    '''simulates removal of an edge by filling with NaNs'''
    graph = graph.copy()
    graph[e,:] = np.Inf
    graph[:,e] = np.Inf
    np.fill_diagonal(graph, 0)
    return graph

def range_minus(n, skip):
    for i in range(n):
        if i == skip:
            continue
        yield i

def robustness(gene):
    n = gene.shape[0]
    times = gene_to_distance_matrix(gene, dists)
    shortest_paths = shortest_path(times, directed=False)
    big_sum = 0
    for removed in range(n):
        times_prime = remove_edge(times, removed)
        shortest_paths_prime = shortest_path(times_prime, directed=False)
        for a in range_minus(n, removed):
            sum_before = 0
            sum_after = 0
            for b in range_minus(n, removed):
                sum_before += shortest_paths[a,b]
                sum_after += shortest_paths_prime[a,b]
            big_sum += 1/sum_before - 1/sum_after
    # TODO  how to deal with perfect robustness? Need to sigmoid or other normalization?
    # biranking might be appropriate here.
    return 1/big_sum if big_sum != 0 else 10000

def fitness(gene):
    #return robustness(gene) - sum_shortest_paths(gene)
    return -sum_shortest_paths(gene)

def crossover(a, b, keep_both=False):
    n = a.shape[0]
    new1 = np.zeros((n,n))
    new2 = np.zeros((n,n))
    for i in range(n):
        for j in range(n):
            coin = randp()
            new1[i,j] = a[i,j] if coin else b[i,j]
            new2[i,j] = b[i,j] if coin else a[i,j]
    if keep_both:
        return normalize_gene(new1), normalize_gene(new2)
    return normalize_gene(new1)

def mutate(gene):
    n = gene.shape[0]
    new_gene = gene + np.random.rand(n, n) * 0.2
    return new_gene

def neighbor(gene):
    ''' apply hypersphere noise,
        aka epsilon ball'''
    n = gene.shape[0]
    noise = np.random.randn(n,n)
    sphere_noise = noise / np.linalg.norm(noise)
    return normalize_gene(gene + sphere_noise * 0.1)

def gene_distance(a, b):
    return np.sqrt(np.sum(np.square(a-b)))


def visualize(gene):
    n = gene.shape[0]
    lines = []
    widths = []
    for i in range(n):
        for j in range(i):
            start = points[i]
            end = points[j]
            weight = gene[j,i]
            lines.append([start, end])
            widths.append(weight)
    visualizer.visualize(lines, widths)






##bene = generate_gene(4)
##print(gene)
##print(bene)
##print(crossover(gene, bene))
##times = gene_to_distance_matrix(gene, dists)
##shortest_paths = shortest_path(times, directed=False)
##
##print(gene)
##print(dists)
##print(times)
##print(fitness_robustness(gene))
