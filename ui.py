"""
Terminal display and UI helpers.
"""
import os
import platform
from typing import List
from business import Business


def clear_screen():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)


def format_amount(n: float) -> str:
    """
    Abbreviate large numbers: k, mil, bil, etc.
    """
    if n >= 1e9:
        return f"{n/1e9:.2f}bil"
    if n >= 1e6:
        return f"{n/1e6:.2f}mil"
    if n >= 1e3:
        return f"{n/1e3:.2f}k"
    return f"{n:.2f}" if not n.is_integer() else f"{int(n)}"


def display_status(cash: float, businesses: List[Business]):
    clear_screen()
    total_rps = sum(b.profit_per_sec() for b in businesses)
    print(f"Cash: ${format_amount(cash):<10}    Total RPS: ${format_amount(total_rps)}\n")
    print("Businesses (cycle progress):")
    bar_len = 10
    for idx, biz in enumerate(businesses, start=1):
        prog = biz.progress()
        fill = int(prog * bar_len)
        bar = '[' + '#' * fill + '-' * (bar_len - fill) + ']'
        mgr = ' [M]' if biz.manager else ''
        cost_str = format_amount(biz.cost())
        rps_str = format_amount(biz.profit_per_sec())
        print(
            f"{idx}. {biz.name:<20}{mgr:<4}"
            f"Owned:{biz.count:<4}"
            f"Cost:${cost_str:<8}"  
            f"RPS:${rps_str:<8}"  
            f"{bar} {int(prog*100):>3}%"
        )
    print()