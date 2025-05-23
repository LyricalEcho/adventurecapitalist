"""
Terminal UI: display formatting and helpers.
"""
import os
import platform
from typing import List
from business import Business


def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def format_amount(n: float) -> str:
    """Abbreviate numbers: k, mil, bil."""
    if n >= 1e9:
        return f"{n/1e9:.2f}bil"
    if n >= 1e6:
        return f"{n/1e6:.2f}mil"
    if n >= 1e3:
        return f"{n/1e3:.2f}k"
    return f"{n:.2f}" if not n.is_integer() else f"{int(n)}"


def display_status(cash: float, businesses: List[Business]):
    clear_screen()
    total = sum(b.profit_per_sec() for b in businesses)
    print(f"Cash: ${format_amount(cash):<10}   Total Revenue Per Cycle: ${format_amount(total)}\n")
    print("Businesses (progress):")
    for idx, biz in enumerate(businesses, 1):
        prog = biz.progress()
        bar = '[' + '#' * int(prog*10) + '-' * (10-int(prog*10)) + ']'  # 10-char
        mgr = ' [M]' if biz.manager else ''
        print(f"{idx}. {biz.name:<18}{mgr:<4} Owned:{biz.count:<4}"
              f" Cost:${format_amount(biz.cost()):<8}"
              f" R/C:${format_amount(biz.profit_per_sec()):<8} {bar} {int(prog*100):>3}%")
    print()