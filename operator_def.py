import json
import numpy as np
import random

import driver_def

class Operator:
    def __init__(self, operator_file, tactics):

        with open(operator_file) as f:
            df = json.load(f)
        self.operator_id = df['operator_id']
        self.home_coord = df['home_coord']

        self.drivers = []
        for driver_info in df['driver_list']:
            driver_id = driver_info['driver_id']
            driver_home_coord_x = int(self.home_coord[0] + np.floor(random.uniform(-5, 6)))
            driver_home_coord_y = int(self.home_coord[1] + np.floor(random.uniform(-5, 6)))
            stock_size = driver_info['stock_size']
            driver = driver_def.Driver(driver_id, [driver_home_coord_x, driver_home_coord_y], stock_size)
            self.drivers.append(driver)

        self.stock_size = df['stock_size']

        self.distribution = df['distribution']

        self.cum_order_count = 0
        self.cum_passing_count = 0

        self.tactics = tactics

    def assign_order(self, current_time, whole_operators, order):
        random_val = random.random()
        cum_dist = np.cumsum(self.distribution)

        for i in range(len(cum_dist)):
            selected_tactics_idx = i
            if random_val <= cum_dist[i]:
                break
        operator_id, driver_id = self.tactics[selected_tactics_idx](self.operator_id, whole_operators, order)
        # print(selected_tactics_idx)
        if driver_id != -1:
            set_result = whole_operators[operator_id].drivers[driver_id].set_order(order, current_time)
            return 0
        else:
            return -1
