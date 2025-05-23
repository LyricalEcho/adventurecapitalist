"""
Defines the Business class and milestone logic.
"""
import time
from constants import MILESTONE_THRESHOLDS

class Business:
    def __init__(self, name, base_cost, base_profit, interval=1.0):
        self.name = name
        self.base_cost = base_cost
        self.base_profit = base_profit
        self.interval = interval
        self.count = 0
        self.manager = False
        self.multiplier = 1.0
        self.last_time = time.time()

    def cost(self):
        return self.base_cost * (1.07 ** self.count)

    def manager_cost(self):
        return self.base_cost * 100

    def profit_per_sec(self):
        return self.base_profit * self.count * self.multiplier

    def ready(self):
        return (time.time() - self.last_time) >= self.interval

    def collect(self):
        if self.count == 0 or not self.ready():
            return 0.0
        earnings = self.base_profit * self.count * self.multiplier
        self.last_time = time.time()
        return earnings

    def progress(self):
        return min((time.time() - self.last_time) / self.interval, 1.0)

    def check_milestone(self):
        if self.count in MILESTONE_THRESHOLDS:
            self.multiplier *= 2