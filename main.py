"""
Main entrypoint: orchestrates game loop and user input.
"""
import time
from business import Business
from save_load import save_game, load_game
from ui import display_status


def main():
    businesses = [
        Business("Lemonade Stand", 4, 1, interval=1),
        Business("Newspaper Delivery", 60, 60, interval=10),
        Business("Car Wash", 720, 540, interval=100),
        Business("Pizza Delivery", 8640, 4320, interval=1000),
        Business("Donut Shop", 103680, 51840, interval=10000),
    ]
    cash = load_game(businesses)
    if cash == 0 and businesses[0].count == 0:
        businesses[0].count = 1
    for biz in businesses:
        biz.last_time = time.time()

    actions = {'1': 'Buy', '2': 'Collect', '3': 'Hire Manager', '4': 'Save & Exit'}

    while True:
        for biz in businesses:
            if biz.manager and biz.ready():
                cash += biz.collect()
        display_status(cash, businesses)
        print("Actions:")
        for k, v in actions.items(): print(f" {k}) {v}")
        choice = input("Select: ")

        if choice == '1':
            try:
                idx = int(input("Business #: ")) - 1
                biz = businesses[idx]
                price = biz.cost()
                if cash >= price:
                    cash -= price
                    biz.count += 1
                    biz.check_milestone()
                    print(f"Purchased 1 {biz.name}! Total: {biz.count}")
                else:
                    print("Insufficient funds.")
            except (IndexError, ValueError):
                print("Invalid selection.")

        elif choice == '2':
            collected = 0.0
            for biz in businesses:
                if not biz.manager:
                    amt = biz.collect()
                    collected += amt
                    cash += amt
            print(f"Collected ${collected} manually.") if collected else print("Nothing to collect.")

        elif choice == '3':
            try:
                idx = int(input("Business #: ")) - 1
                biz = businesses[idx]
                if biz.manager:
                    print("Manager already hired.")
                else:
                    cost = biz.manager_cost()
                    if cash >= cost:
                        cash -= cost
                        biz.manager = True
                        print(f"Manager hired for {biz.name}.")
                    else:
                        print("Insufficient funds for manager.")
            except (IndexError, ValueError):
                print("Invalid selection.")

        elif choice == '4':
            save_game(cash, businesses)
            print("Game saved. Goodbye!")
            break

        else:
            print("Invalid action.")

        time.sleep(1)

if __name__ == '__main__':
    main()
