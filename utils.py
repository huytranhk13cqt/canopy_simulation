import math

from colorama import Fore, Style, init

from cano import *

# CONSTANT
TOTAL_PIXELS = 300 * 300
ATTEMPS = 3

# Initialize colorama
init(autoreset=True)


# 3.1 code ref 
# Function 0: Get mode choice
def get_mode_choice():
    print(Fore.GREEN + "┌" + "─" * 56 + "┐")
    print(Fore.GREEN + "│ Choose mode:                                           │")
    print(Fore.GREEN + "│ 1. Manual input                                        │")
    print(Fore.GREEN + "│ 2. File input                                          │")
    print(Fore.GREEN + "└" + "─" * 56 + "┘")
    choice = input(
        Fore.WHITE + "Enter your choice (1 or 2): " + Style.RESET_ALL)
    if choice in ['1', '2']:
        return 'manual' if choice == '1' else 'file'
    else:
        print(Fore.RED + "╔" + "═" * 56 + "╗")
        print(Fore.RED + "║ Invalid choice. Please enter 1 or 2.                   ║")
        print(Fore.RED + "╚" + "═" * 56 + "╝")
        return get_mode_choice()  # Recursively call the function for invalid input

# 3.2 code ref
# Function 1: Get valid input from user
def get_valid_input(prompt, error_message, condition_func, attempts=ATTEMPS):
    if attempts <= 0:
        print(Fore.RED + "Maximum attempts reached. Exiting...")
        return None

    try:
        print(Fore.GREEN + "┌" + "─" * 56 + "┐")
        print(Fore.GREEN + f"│ {prompt:<52} ")
        print(Fore.GREEN + "└" + "─" * 56 + "┘")
        value = int(input(Fore.WHITE + "Enter your choice: "))

        if condition_func(value):
            return value

        print(Fore.RED + "╔" + "═" * 56 + "╗")
        print(Fore.RED + f"║ {error_message:<52} ")
        print(Fore.RED + "╚" + "═" * 56 + "╝")
    except ValueError:
        print(Fore.RED + "╔" + "═" * 56 + "╗")
        print(Fore.RED + "║ Invalid input. Please enter a number.           ║")
        print(Fore.RED + "╚" + "═" * 56 + "╝")

    return get_valid_input(prompt, error_message, condition_func, attempts - 1)

# 3.3 code ref
# Function 2: Get map shape
def get_map_shape(num_blocks, attempts=ATTEMPS):
    # 3.3.1 code ref
    def is_valid_rows(x):
        return 0 < x <= num_blocks

    if attempts <= 0:
        print(Fore.RED + "Maximum attempts reached. Exiting...")
        return None

    try:
        rows = get_valid_input(f"Enter number of rows (1-{num_blocks})",
                               f"Please enter a number between 1 and {num_blocks}.", is_valid_rows, attempts=ATTEMPS)
        cols = num_blocks // rows

        if num_blocks % rows == 0:
            return (rows, cols)
        else:
            print(Fore.YELLOW + "╔" + "═" * 56 + "╗")
            print(Fore.YELLOW + f"║ Invalid shape. {num_blocks} is not divisible by {rows}." + " " * (
                50 - len(f"Invalid shape. {num_blocks} is not divisible by {rows}.")) + "║")
            print(Fore.YELLOW + "╚" + "═" * 56 + "╝")
            return get_map_shape(num_blocks, attempts - 1)
    except ValueError:
        print(Fore.RED + "╔" + "═" * 56 + "╗")
        print(Fore.RED + "║ Invalid input. Please enter a number.                ║")
        print(Fore.RED + "╚" + "═" * 56 + "╝")
        return get_map_shape(num_blocks, attempts - 1)

# 3.4 code ref  
# Function 3: Get block distribution
def get_block_distribution(num_blocks):
    # 3.4.1 code ref
    def is_valid_yards(x):
        return 0 <= x <= num_blocks

    # 3.4.2 code ref
    def is_valid_grounds(x):
        return 0 <= x <= num_blocks - yards

    try:
        yards = get_valid_input(f"Enter number of Yard blocks  (0-{num_blocks})",
                                f"Please enter a number between 0 and {num_blocks}.", is_valid_yards, attempts=ATTEMPS)
        grounds = get_valid_input(f"Enter number of Ground blocks (0-{num_blocks - yards})",
                                  f"Please enter a number between 0 and {num_blocks - yards}.", is_valid_grounds, attempts=ATTEMPS)
        rivers = num_blocks - yards - grounds
        print()
        print(Fore.CYAN + "╔" + "═" * 50 + "╗")
        print(Fore.CYAN + f"║ Number of River blocks: {rivers:<28} ")
        print(Fore.CYAN + "╚" + "═" * 50 + "╝")
        print()
        return (yards, grounds, rivers)
    except ValueError:
        print(Fore.RED + "Maximum attempts reached. Exiting...")
        return None

# 3.5 code ref
# Function 4: Calculate block size (block is square)
def calculate_block_size(num_blocks):
    pixels_per_block = TOTAL_PIXELS // num_blocks
    block_size = int(math.sqrt(pixels_per_block))
    return max(10, min(100, block_size))

# 3.6 code ref
# Function 5: Calculate max items (houses and trees can be added to Yard and Ground blocks)
def calculate_max_items(blocks):
    max_houses = sum(
        block.max_houses for block in blocks if block.block_type == 'Yard')
    max_trees = sum(
        block.max_trees for block in blocks if block.block_type == 'Ground')
    return max_houses, max_trees
