"""
Handles persistence: save and load functions.
"""
import json
import os
import time
from constants import SAVE_FILE

from business import Business


def save_game(cash, businesses):
    payload = {'cash': cash, 'timestamp': time.time(), 'businesses': []}
    for b in businesses:
        payload['businesses'].append({
            'count': b.count,
            'manager': b.manager,
            'multiplier': b.multiplier,
            'last_time': b.last_time
        })
    with open(SAVE_FILE, 'w') as f:
        json.dump(payload, f)


def load_game(businesses):
    if not os.path.isfile(SAVE_FILE):
        return 0.0
    with open(SAVE_FILE, 'r') as f:
        data = json.load(f)
    cash = data.get('cash', 0.0)
    now = time.time()
    for biz, saved in zip(businesses, data.get('businesses', [])):
        biz.count = saved['count']
        biz.manager = saved['manager']
        biz.multiplier = saved['multiplier']
        biz.last_time = saved['last_time']
        if biz.manager and biz.count > 0:
            elapsed = now - biz.last_time
            cycles = int(elapsed // biz.interval)
            if cycles:
                cash += cycles * biz.base_profit * biz.count * biz.multiplier
                biz.last_time += cycles * biz.interval
    return cash