#!/usr/bin/env python3
import time
import os
import platform
import json

SAVE_FILE = 'savegame.json'

class Business:
    MILESTONES = [25, 50, 100, 250, 500, 1000]

    def __init__(self, name: str, base_cost: float, base_profit: float, interval: float = 1.0):
        self.name = name
        self.base_cost = base_cost
        self.base_profit = base_profit
        self.interval = interval              # seconds per production cycle
        self.count = 0
        self.manager = False
        self.multiplier = 1.0                 # Profit multiplier for milestones
        self.last_time = time.time()

    def cost(self) -> float:
        # Cost to buy next unit increases by 7%
        return self.base_cost * (1.07 ** self.count)

    def manager_cost(self) -> float:
        # Static manager cost: 100× base cost
        return self.base_cost * 100

    def profit_per_sec(self) -> float:
        # Profit per second factoring in multiplier
        return self.base_profit * self.count * self.multiplier

    def ready(self) -> bool:
        return (time.time() - self.last_time) >= self.interval

    def collect(self) -> float:
        # Collect profit if ready, reset cycle
        if self.count == 0 or not self.ready():
            return 0.0
        earnings = self.base_profit * self.count * self.multiplier
        self.last_time = time.time()
        return earnings

    def progress(self) -> float:
        return min((time.time() - self.last_time) / self.interval, 1.0)

    def check_milestone(self):
        # Double profits at milestone counts
        if self.count in Business.MILESTONES:
            self.multiplier *= 2


def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def save_game(cash: float, businesses: list[Business]):
    data = {
        'cash': cash,
        'timestamp': time.time(),
        'businesses': []
    }
    for b in businesses:
        data['businesses'].append({
            'count': b.count,
            'manager': b.manager,
            'multiplier': b.multiplier,
            'last_time': b.last_time
        })
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)
    except IOError:
        pass  # ignore save errors


def load_game(businesses: list[Business]):
    cash = 0.0
    if not os.path.isfile(SAVE_FILE):
        return cash

    try:
        with open(SAVE_FILE, 'r') as f:
            data = json.load(f)
    except (IOError, json.JSONDecodeError):
        return cash

    cash = data.get('cash', 0.0)
    saved = data.get('businesses', [])
    now = time.time()

    # Restore each business state
    for b, s in zip(businesses, saved):
        b.count = s.get('count', 0)
        b.manager = s.get('manager', False)
        b.multiplier = s.get('multiplier', 1.0)
        b.last_time = s.get('last_time', now)
        # Auto-earn offline for managed businesses
        if b.manager and b.count > 0:
            elapsed = now - b.last_time
            cycles = int(elapsed // b.interval)
            if cycles > 0:
                cash += cycles * b.base_profit * b.count * b.multiplier
                # advance last_time by full cycles
                b.last_time += cycles * b.interval
    return cash


def display_status(cash: float, businesses: list[Business]):
    clear_screen()
    total_rps = sum(b.profit_per_sec() for b in businesses)
    print(f"Cash: ${cash:,.2f}    Total RPS: ${total_rps:,.2f}\n")
    print("Businesses (progress to next harvest):")
    bar_len = 10
    for i, b in enumerate(businesses, start=1):
        prog = b.progress()
        filled = int(prog * bar_len)
        bar = '[' + '#' * filled + '-' * (bar_len - filled) + ']'
        mgr_flag = ' [M]' if b.manager else ''
        print(
            f" {i}) {b.name:<15}{mgr_flag:<4} "
            f"Owned: {b.count:<4} "
            f"Cost: ${b.cost():<10.2f} "
            f"RPS: ${b.profit_per_sec():<6.2f} "
            f"{bar} {int(prog*100):>3}%"
        )
    print()


def main():
    # Setup businesses with intervals scaled by 10×
    businesses = [
        Business("Lemonade Stand",     4,      1,     interval=1),
        Business("Newspaper Delivery", 60,     60,    interval=10),
        Business("Car Wash",          720,    540,   interval=100),
        Business("Pizza Delivery",    8640,   4320,  interval=1000),
        Business("Donut Shop",        103680, 51840, interval=10000),
    ]
    # Load or initialize game
    cash = load_game(businesses)
    if cash == 0.0 and businesses[0].count == 0:
        businesses[0].count = 1
    # Reset timers to now
    for b in businesses:
        b.last_time = time.time()

    while True:
        # Auto-collect for managed businesses
        for b in businesses:
            if b.manager and b.ready():
                cash += b.collect()

        display_status(cash, businesses)
        print("Choose an action:")
        print("  1) Buy Business")
        print("  2) Collect Profits")
        print("  3) Hire Manager")
        print("  4) Save & Exit")
        choice = input("\nEnter choice (1-4): ")

        if choice == '1':
            try:
                idx = int(input("Enter business number to buy: ")) - 1
                b = businesses[idx]
                price = b.cost()
                if cash >= price:
                    cash -= price
                    b.count += 1
                    b.check_milestone()
                    print(f"\nPurchased 1 {b.name}! You now own {b.count}.")
                else:
                    print("\nNot enough cash to purchase.")
            except (ValueError, IndexError):
                print("\nInvalid selection.")
            time.sleep(1)

        elif choice == '2':
            total = 0.0
            for b in businesses:
                if not b.manager:
                    amt = b.collect()
                    if amt > 0:
                        total += amt
                        cash += amt
            if total > 0:
                print(f"\nCollected ${total:,.2f} manually from ready businesses!")
            else:
                print("\nNo unmanaged businesses ready yet.")
            time.sleep(1)

        elif choice == '3':
            try:
                idx = int(input("Enter business number to hire manager for: ")) - 1
                b = businesses[idx]
                if b.manager:
                    print(f"\n{b.name} already has a manager.")
                else:
                    m_cost = b.manager_cost()
                    if cash >= m_cost:
                        cash -= m_cost
                        b.manager = True
                        print(f"\nHired manager for {b.name}! Automating collections.")
                    else:
                        print(f"\nNot enough cash (${m_cost:,.2f}) to hire manager.")
            except (ValueError, IndexError):
                print("\nInvalid selection.")
            time.sleep(1)

        elif choice == '4':
            save_game(cash, businesses)
            print("\nGame saved! Goodbye.")
            break

        else:
            print("\nInvalid choice.")
            time.sleep(1)


if __name__ == "__main__":
    main()
