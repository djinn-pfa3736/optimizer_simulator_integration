import sys

import numpy as np
import matplotlib.pyplot as plt

import glob
import random

import pickle

import pdb

import simulator

class Optimizer:

    def __init__(self, generation_num, map_file, demands_distribution_pickle, \
                    temporal_distribution_pickle, total_order_num, appli_ratio, \
                    operator_file_list, simulation_length, simulation_start):

        self.simulation_start = simulation_start
        self.simulation_length = simulation_length

        self.world = simulator.World(map_file, operator_file_list, demands_distribution_pickle, \
            temporal_distribution_pickle, total_order_num, appli_ratio, simulation_start)

        self.operators = self.world.operators

        self.generation_num = generation_num

    def optimize(self, elite_ratio, crossed_gene_num, crossed_pos_idx):
        self.initialize_optimization()
        generation_count = 0
        while generation_count < self.generation_num:
            self.optimize_one_step(elite_ratio, crossed_gene_num, crossed_pos_idx)
            generation_count += 1

    def optimize_one_step(self, elite_ratio, crossed_gene_num, crossed_pos_idx):
        self.evaluate()
        self.create_next_generation(elite_ratio, crossed_gene_num, crossed_pos_idx)
        self.world.initialize_simulation(self.gene_pool)

    def initialize_optimization(self):

        self.world.calc_scores(self.simulation_length)

        self.gene_pool = []
        for operator in self.world.operators:
            self.gene_pool.append(operator.distribution)
        self.gene_pool = np.array(self.gene_pool)
        self.efficiency_list, operator_wait_time, phone_cancelled_num, appli_cancelled_num = self.world.report()
        self.efficiency_list = np.array(self.efficiency_list)

        sorted_idx = np.argsort(-1*self.efficiency_list)
        self.gene_pool = self.gene_pool[sorted_idx]
        self.efficiency_list = self.efficiency_list[sorted_idx]

        # pdb.set_trace()

    def evaluate(self):
        self.world.calc_scores(self.generation_num)
        self.efficiency_list, operator_wait_time, phone_cancelled_num, appli_cancelled_num = self.world.report()
        self.efficiency_list = np.array(self.efficiency_list)

        sorted_idx = np.argsort(-1*self.efficiency_list)
        self.gene_pool = np.array(self.gene_pool)
        self.gene_pool = self.gene_pool[sorted_idx]
        self.efficiency_list = self.efficiency_list[sorted_idx]

    def create_next_generation(self, elite_ratio, crossed_gene_num, crossed_pos_idx):
        elite_range = int(np.floor(len(self.efficiency_list)*elite_ratio))
        idx = random.sample(range(elite_range+1), 2)

        next_gene_pool = []

        for i in range(crossed_gene_num):
            gene1 = self.gene_pool[idx[0]]
            gene2 = self.gene_pool[idx[1]]
            new_gene = self.cross_over_split(gene1, gene2, crossed_pos_idx)
            next_gene_pool.append(new_gene)

        for i in range(len(self.gene_pool) - crossed_gene_num):

            mutation_flag = 1 if random.random() < 0.5 else 0
            if mutation_flag == 1:
                next_gene = self.one_point_mutation(self.gene_pool[i])
            else:
                next_gene = self.gene_pool[i]
            next_gene_pool.append(next_gene)

        self.gene_pool = next_gene_pool

        # pdb.set_trace()

    def cross_over_split(self, gene1, gene2, pos_idx):
        new_gene = np.zeros_like(gene1)
        new_gene[0:pos_idx] = gene1[0:pos_idx]
        new_gene[pos_idx:-1] = gene2[pos_idx:-1]

        new_gene = np.array(new_gene)
        new_gene = new_gene/np.sum(new_gene)

        return new_gene

    def one_point_mutation(self, gene):
        sd = np.sqrt(np.var(gene))
        pos_idx = int(np.floor(random.random()*len(gene)))
        sign = 1 if random.random() < 0.5 else -1
        new_gene = gene.copy()
        new_gene[pos_idx] += sign*sd

        new_gene = np.array(new_gene)
        new_gene = new_gene/np.sum(new_gene)

        return new_gene

if __name__ == '__main__':

    operator_file_list = glob.glob('operator_*.json')
    optimizer = Optimizer(500, './map_file.csv', 'spatial_temporal_grid.pickle', \
            'occuring_distribution.pickle', 600, 0.2, operator_file_list, 360, 21*60)
    optimizer.optimize(0.3, 1, 3)
