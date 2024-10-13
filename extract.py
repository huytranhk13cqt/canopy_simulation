# 5.0 code ref
def extract_values_from_file(file_path='input.txt'):
    with open(file_path, 'r') as file:
        for line in file:
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                if key == "Num Blocks":
                    num_blocks = int(value)
                elif key == "Num Rows":
                    num_rows = int(value)
                elif key == "Num Block Yards":
                    num_yards = int(value)
                elif key == "Num Block Ground":
                    num_grounds = int(value)
                elif key == "Num Block River":
                    num_rivers = int(value)
                elif key == "Num houses of each Block Yard":
                    num_houses = int(value)
                elif key == "Num trees of each Block Ground":
                    num_trees = int(value)
                elif key == "The time (0-24) to view Thermal Map":
                    specific_time = int(value)
    return (num_blocks, num_rows, num_yards, num_grounds, num_rivers, num_houses, num_trees, specific_time)
