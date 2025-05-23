"""
Handles persistence: save/load and offline earnings.
"""
import json
import os
import time
from constants import SAVE_FILE
from business import Business


def save_game(cash, businesses):
    """Serialize game state to JSON file."""
    payload = {
        'cash': cash,
        'timestamp': time.time(),
        'businesses': [
            {'count': b.count, 'manager': b.manager, 'multiplier': b.multiplier, 'last_time': b.last_time}
            for b in businesses
        ]
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(payload, f)


def load_game(businesses):
    """Load game state, restoring businesses and granting offline earnings."""
    if not os.path.exists(SAVE_FILE):
        return 0.0
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)

    cash = data.get('cash', 0.0)
    now = time.time()
    for biz, saved in zip(businesses, data['businesses']):
        biz.count = saved['count']
        biz.manager = saved['manager']
        biz.multiplier = saved['multiplier']
        biz.last_time = saved['last_time']
        # grant offline cycles for managed biz
        if biz.manager and biz.count:
            cycles = int((now - biz.last_time) // biz.interval)
            if cycles:
                cash += cycles * biz.base_profit * biz.count * biz.multiplier
                biz.last_time += cycles * biz.interval
    return cash
