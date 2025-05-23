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
        """Cost for next unit (7% increase per owned unit)."""
        return self.base_cost * (1.07 ** self.count)

    def manager_cost(self):
        """Flat cost to hire a manager (100× base cost)."""
        return self.base_cost * 100

    def profit_per_sec(self):
        """Revenue per cycle factoring milestone multiplier."""
        return self.base_profit * self.count * self.multiplier

    def ready(self):
        """Check if harvest interval has passed."""
        return (time.time() - self.last_time) >= self.interval

    def collect(self):
        """Collect profit if ready, reset timer."""
        if self.count == 0 or not self.ready():
            return 0.0
        earnings = self.base_profit * self.count * self.multiplier
        self.last_time = time.time()
        return earnings

    def progress(self):
        """Fraction [0.0, 1.0] of the current interval completed."""
        return min((time.time() - self.last_time) / self.interval, 1.0)

    def check_milestone(self):
        """Double multiplier on reaching milestone thresholds."""
        if self.count in MILESTONE_THRESHOLDS:
            self.multiplier *= 2