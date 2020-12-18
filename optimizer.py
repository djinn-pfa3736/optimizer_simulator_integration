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
                    temporal_distribution_pickle, total_order_num, appli_ratio, operator_file_list, simulation_length, simulation_start):

        self.simulation_start = simulation_start
        self.simulation_length = simulation_length

        self.world = simulator.World(map_file, operator_file_list, demands_distribution_pickle, \
            temporal_distribution_pickle, total_order_num, appli_ratio, simulation_start)

        self.operators = self.world.operators

        self.generation_num = generation_num

    def initialize_optimization(self):

        self.world.calc_scores(self.generation_num)

        self.gene_pool = []
        for operator in self.world.operators:
            self.gene_pool.append(operator.distribution)

        efficiency_list, operator_wait_time, phone_cancelled_num, appli_cancelled_num = self.world.report()
        pdb.set_trace()

if __name__ == '__main__':

    optimizer = Optimizer(500, './map_file.csv', 'spatial_temporal_grid.pickle', \
            'occuring_distribution.pickle', 600, 0.2, ['operator_0.json'], 360, 21*60)

    optimizer.initialize_optimization()
