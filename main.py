"""
Main loop and user interactions.
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
    if not cash and not businesses[0].count:
        businesses[0].count = 1
    for biz in businesses:
        biz.last_time = time.time()

    actions = {'1': 'Buy Business', '2': 'Collect', '3': 'Hire Manager', '4': 'Save & Exit'}

    while True:
        # auto-collect for managers
        for biz in businesses:
            if biz.manager and biz.ready():
                cash += biz.collect()

        display_status(cash, businesses)
        for key, act in actions.items(): print(f"{key}) {act}")
        choice = input("> ")

        if choice == '1':
            idx = int(input("Business #: ")) - 1
            if 0 <= idx < len(businesses):
                biz = businesses[idx]
                cost = biz.cost()
                if cash >= cost:
                    cash -= cost
                    biz.count += 1
                    biz.check_milestone()
                    print(f"Bought 1 {biz.name}, now {biz.count}.")
                else:
                    print("Not enough cash.")
            else:
                print("Invalid business #.")

        elif choice == '2':
            total_col = 0
            for biz in businesses:
                if not biz.manager:
                    amt = biz.collect()
                    total_col += amt
                    cash += amt
            print(f"Collected ${total_col}.") if total_col else print("Nothing ready.")

        elif choice == '3':
            idx = int(input("Business #: ")) - 1
            if 0 <= idx < len(businesses):
                biz = businesses[idx]
                if not biz.manager:
                    m_cost = biz.manager_cost()
                    if cash >= m_cost:
                        cash -= m_cost
                        biz.manager = True
                        print(f"Manager for {biz.name} hired.")
                    else:
                        print("Insufficient funds.")
                else:
                    print("Already has manager.")
            else:
                print("Invalid business #.")

        elif choice == '4':
            save_game(cash, businesses)
            print("Game saved.")
            break

        else:
            print("Invalid action.")

        time.sleep(1)

if __name__ == '__main__':
    main()
