import random

from colorama import Fore, Style, init
from tabulate import tabulate
from utils import *
from visualization import *

from cano import *
from extract import extract_values_from_file

# CONSTANT
TOTAL_PIXELS = 300 * 300
ATTEMPS = 3

# Initialize colorama
init(autoreset=True)

# 6.1 code ref
# Function 6: Add items to blocks


def add_items_to_blocks(blocks, num_houses, num_trees):
    yard_blocks = [block for block in blocks if block.block_type == 'Yard']
    ground_blocks = [block for block in blocks if block.block_type == 'Ground']

    houses_added = 0
    trees_added = 0

    # Add houses
    while houses_added < num_houses and yard_blocks:
        block = random.choice(yard_blocks)
        house_size = block.house_size
        free_space = block._find_random_free_space(house_size)
        if free_space:
            block.add_item('House', free_space)
            houses_added += 1
        else:
            yard_blocks.remove(block)

    # Add trees
    while trees_added < num_trees and ground_blocks:
        block = random.choice(ground_blocks)
        tree_size = block.tree_size
        free_space = block._find_random_free_space(tree_size)
        if free_space:
            block.add_item('Tree', free_space)
            trees_added += 1
        else:
            ground_blocks.remove(block)

    return houses_added, trees_added

# 6.2 code ref
# Function 7: Add roads to blocks


def add_roads_to_blocks(blocks, map_shape):
    rows, cols = map_shape
    for i, block in enumerate(blocks):
        if block.block_type != 'River':
            if i < cols or (i >= cols and blocks[i - cols].block_type != 'River'):
                block.add_road('top')
            if i >= cols * (rows - 1) or (i < cols * (rows - 1) and blocks[i + cols].block_type != 'River'):
                block.add_road('bottom')
            if i % cols == 0 or (i % cols != 0 and blocks[i - 1].block_type != 'River'):
                block.add_road('left')
            if (i + 1) % cols == 0 or ((i + 1) % cols != 0 and blocks[i + 1].block_type != 'River'):
                block.add_road('right')

# 6.3 code ref
# Function 12: Ask for simulation


def ask_for_simulation():
    print(Fore.GREEN + "┌" + "─" * 56 + "┐")
    print(Fore.GREEN + "│ Do you want to simulate the thermal view over time?    │")
    print(Fore.GREEN + "└" + "─" * 56 + "┘")
    choice = input(Fore.WHITE + "Enter your choice (y/n): " +
                   Style.RESET_ALL).lower()
    if choice in ['y', 'n']:
        return choice == 'y'
    else:
        print(Fore.RED + "╔" + "═" * 56 + "╗")
        print(Fore.RED + "║ Invalid choice. Please enter 'y' or 'n'.               ║")
        print(Fore.RED + "╚" + "═" * 56 + "╝")
        return ask_for_simulation()


# 6.4 code ref
def main():
    # 6.4.1 code ref
    mode = get_mode_choice()

    # 6.4.2 code ref
    if mode == 'manual':
        def is_positive(x):
            return x > 0

        num_blocks = get_valid_input("Enter the number of blocks",
                                     "Please enter a positive number.", is_positive, attempts=ATTEMPS)
        map_shape = get_map_shape(num_blocks, attempts=ATTEMPS)
        block_distribution = get_block_distribution(num_blocks)
        block_size = calculate_block_size(num_blocks)
    else:
        # 6.4.3 code ref
        num_blocks, num_rows, num_yards, num_grounds, num_rivers, num_houses, num_trees, specific_time = extract_values_from_file(
            'input.txt')
        map_shape = (num_rows, num_blocks // num_rows)
        block_distribution = (num_yards, num_grounds, num_rivers)
        block_size = calculate_block_size(num_blocks)

    # 6.4.4 code ref
    blocks = []
    block_types = ['Yard'] * block_distribution[0] + ['Ground'] * \
        block_distribution[1] + ['River'] * block_distribution[2]
    random.shuffle(block_types)

    for i in range(num_blocks):
        row = i // map_shape[1]
        col = i % map_shape[1]
        topleft = (col * block_size, row * block_size)
        block = Block(block_size, topleft, block_types[i], i)
        blocks.append(block)

    # 6.4.5 code ref
    add_roads_to_blocks(blocks, map_shape)

    # 6.4.6 code ref
    max_houses, max_trees = calculate_max_items(blocks)

    # 6.4.7 code ref
    if mode == 'manual':
        def is_valid_houses(x):
            return 0 <= x <= max_houses

        def is_valid_trees(x):
            return 0 <= x <= max_trees

        num_houses = get_valid_input(f"Enter number of houses (0-{max_houses})",
                                     f"Please enter a number between 0 and {max_houses}.", is_valid_houses, attempts=ATTEMPS)
        num_trees = get_valid_input(f"Enter number of trees (0-{max_trees})",
                                    f"Please enter a number between 0 and {max_trees}.", is_valid_trees, attempts=ATTEMPS)
    else:
        num_houses = min(num_houses, max_houses)
        num_trees = min(num_trees, max_trees)

    # 6.4.8 code ref
    houses_added, trees_added = add_items_to_blocks(
        blocks, num_houses, num_trees)

    # 6.4.9 code ref
    print()
    print(Fore.CYAN + "╔" + "═" * 56 + "╗")
    print(Fore.CYAN + "║              Map Configuration              ")
    print(Fore.CYAN + "╚" + "═" * 56 + "╝")

    table_data = [
        ["Parameter", "Value"],
        ["Map shape", f"{map_shape[0]} x {map_shape[1]}"],
        ["Block size", f"{block_size} px"],
        ["Houses added", f"{houses_added}"],
        ["Trees added", f"{trees_added}"],
        ["Requested houses", f"{num_houses}"],
        ["Requested trees", f"{num_trees}"]
    ]

    print(tabulate(table_data, headers="firstrow", tablefmt="fancy_grid"))

    # 6.4.10 code ref
    if houses_added < num_houses:
        print(Fore.YELLOW + "╔" + "═" * 56 + "╗")
        print(Fore.YELLOW +
              f"║ Only {houses_added} houses could be added due to space   ")
        print(Fore.YELLOW + "║ limitations.                                  ")
        print(Fore.YELLOW + "╚" + "═" * 56 + "╝")

    if trees_added < num_trees:
        print(Fore.YELLOW + "╔" + "═" * 56 + "╗")
        print(Fore.YELLOW +
              f"║ Only {trees_added} trees could be added due to space    ")
        print(Fore.YELLOW + "║ limitations.                                  ")
        print(Fore.YELLOW + "╚" + "═" * 56 + "╝")

    # 6.4.11 code ref
    if mode == 'manual':
        time = get_valid_input(
            "🌞 Enter the time (0-24) to view the thermal map",
            "Please enter a number between 0 and 24.", lambda x: 0 <= x <= 24, attempts=ATTEMPS)
    else:  # mode == 'file'
        time = specific_time

    # 6.4.12 code ref
    update_temperatures(blocks, time)

    # 6.4.13 code ref
    generate_and_display_views(blocks, block_size, map_shape, num_blocks, time)

    # 6.4.14 code ref
    if ask_for_simulation():
        animate_thermal_view_func(blocks, block_size, map_shape, num_blocks)


if __name__ == "__main__":
    main()
