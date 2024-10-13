import math
import random
from typing import List, Union

import numpy as np

# 1.0 code ref
# CONSTANTS
TREE_INITIAL_TEMP = 16
HOUSE_INITIAL_TEMP = 19
ROAD_INITIAL_TEMP = 35
YARD_INITIAL_TEMP = 24.0
GROUND_INITIAL_TEMP = 28.0
RIVER_INITIAL_TEMP = 10
T_PEAK = 14
EFFECT_RATE = 0.2
GREY = [128, 128, 128]
BROWN = [153, 76, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
YELLOW = [255, 255, 0]
BLACK = [0, 0, 0]

ATTEMPTS = 100


# 1.1 code ref
class ThermalItem:
    def __init__(self, initial_temp, ambient_temp):
        self.initial_temp = initial_temp
        self.current_temp = initial_temp
        self.t_mean = (initial_temp + ambient_temp)/2
        self.t_amp = EFFECT_RATE * self.t_mean
        self.t_peak = T_PEAK

    # 1.1.1 code ref
    def update_temperature(self, t):
        self.current_temp = self.t_mean + self.t_amp * \
            math.cos(2 * math.pi / 24 * (t - self.t_peak))

# 1.2 code ref
class Tree(ThermalItem):
    def __init__(self, pos, size, ambient_temp):
        super().__init__(initial_temp=TREE_INITIAL_TEMP, ambient_temp=ambient_temp)
        self.pos = pos
        self.size = size
        self.rgb = np.array(GREEN)

    # 1.2.1 code ref
    def get_image(self):
        return np.ones((self.size, self.size, 3), dtype=np.uint8) * self.rgb

    # 1.2.2 code ref
    def get_topleft(self):
        return self.pos

# 1.3 code ref
class House(ThermalItem):
    def __init__(self, pos, size, ambient_temp):
        super().__init__(initial_temp=HOUSE_INITIAL_TEMP, ambient_temp=ambient_temp)
        self.pos = pos
        self.size = size
        self.rgb = np.array(YELLOW)  # Yellow

    # 1.3.1 code ref
    def get_image(self):
        return np.ones((self.size, self.size, 3), dtype=np.uint8) * self.rgb

    # 1.3.2 code ref
    def get_topleft(self):
        return self.pos

# 1.4 code ref
class Road(ThermalItem):
    def __init__(self, pos, length, orientation, ambient_temp):
        super().__init__(initial_temp=ROAD_INITIAL_TEMP, ambient_temp=ambient_temp)
        self.pos = pos
        self.length = length
        self.orientation = orientation
        self.rgb = np.array(BLACK)
        self.width = 5 if orientation == 'vertical' else length
        self.height = 5 if orientation == 'horizontal' else length

    # 1.4.1 code ref
    def get_image(self):
        return np.ones((self.height, self.width, 3), dtype=np.uint8) * self.rgb

    # 1.4.2 code ref
    def get_topleft(self):
        return self.pos

# 2.0 code ref
class Block:
    # 2.1 code ref
    BLOCK_TYPES = {
        'Yard': (np.array(GREY), YARD_INITIAL_TEMP),
        'Ground': (np.array(BROWN), GROUND_INITIAL_TEMP),
        'River': (np.array(BLUE), RIVER_INITIAL_TEMP)
    }

    # 2.2 code ref
    def __init__(self, size, topleft, block_type, block_number):
        self.size = size
        self.topleft = topleft
        self.items: List[Union[Tree, House, Road]] = []
        self.block_type = block_type
        self.block_number = block_number
        self.occupied_spaces = np.zeros((size, size), dtype=bool)
        self.rgb, self.initial_temp = self.BLOCK_TYPES[block_type]
        self.current_temp = self.initial_temp
        self.t_mean = self.initial_temp
        self.t_amp = EFFECT_RATE * self.t_mean
        self.t_peak = T_PEAK
        self.house_size = int(size * 0.3)
        self.tree_size = int(size * 0.1)   
        self.max_houses = (size // self.house_size) ** 2
        self.max_trees = (size // self.tree_size) ** 2

    # 2.3 code ref
    def add_item(self, item_type, pos=None):
        if item_type == 'Tree' and self.block_type == 'Ground':
            if len([item for item in self.items if isinstance(item, Tree)]) >= self.max_trees:
                return False
            return self._add_house_or_tree('Tree', self.tree_size, pos)
        elif item_type == 'House' and self.block_type == 'Yard':
            if len([item for item in self.items if isinstance(item, House)]) >= self.max_houses:
                return False
            return self._add_house_or_tree('House', self.house_size, pos)
        else:
            return False

    # 2.4 code ref
    def _add_house_or_tree(self, item_type, size, pos=None):
        if pos is None:
            pos = self._find_random_free_space(size)

        if pos and self._is_space_free(pos, (size, size)):
            if item_type == 'Tree':
                self.items.append(Tree(pos, size, self.initial_temp))
            else:
                self.items.append(House(pos, size, self.initial_temp))
            self._mark_occupied(pos, (size, size))
            return True
        return False

    # 2.5 code ref
    def _find_random_free_space(self, size, attempts=ATTEMPTS):
        if attempts <= 0:
            return None

        x = random.randint(0, self.size - size)
        y = random.randint(0, self.size - size)

        if self._is_space_free((x, y), (size, size)):
            return (x, y)

        return self._find_random_free_space(size, attempts - 1)

    # 2.6 code ref
    def _is_space_free(self, pos, size):
        x, y = pos
        width, height = size
        if x + width > self.size or y + height > self.size:
            return False
        return not np.any(self.occupied_spaces[x:x+width, y:y+height])

    # 2.7 code ref
    def _mark_occupied(self, pos, size):
        x, y = pos
        width, height = size
        self.occupied_spaces[x:x+width, y:y+height] = True

    # 2.8 code ref
    def add_road(self, position):
        if self.block_type == 'River':
            return False

        if position in ['top', 'bottom']:
            length = self.size
            orientation = 'horizontal'
            pos = (0, 0) if position == 'top' else (0, self.size - 5)
        elif position in ['left', 'right']:
            length = self.size
            orientation = 'vertical'
            pos = (0, 0) if position == 'left' else (self.size - 5, 0)
        else:
            raise ValueError(
                "Invalid position. Choose 'top', 'bottom', 'left', or 'right'.")

        road = Road(pos, length, orientation, self.initial_temp)
        self.items.append(road)
        self._mark_occupied(pos, (road.width, road.height))
        return True

    # 2.9 code ref
    def generate_rgb_view(self):
        grid = np.ones((self.size, self.size, 3), dtype=np.uint8) * self.rgb
        for item in self.items:
            topleft = item.get_topleft()
            img = item.get_image()
            cx_start, ry_start = topleft
            cx_stop = cx_start + img.shape[1]
            ry_stop = ry_start + img.shape[0]
            grid[ry_start:ry_stop, cx_start:cx_stop] = img
        return grid

    # 2.10 code ref
    def generate_thermal_view(self):
        grid = np.full((self.size, self.size), self.current_temp)
        for item in self.items:
            topleft = item.get_topleft()
            cx_start, ry_start = topleft
            if isinstance(item, (Tree, House)):
                cx_stop = cx_start + item.size
                ry_stop = ry_start + item.size
                grid[ry_start:ry_stop, cx_start:cx_stop] = item.current_temp
            elif isinstance(item, Road):
                cx_stop = cx_start + item.width
                ry_stop = ry_start + item.height
                grid[ry_start:ry_stop, cx_start:cx_stop] = item.current_temp
        return grid

    # 2.11 code ref
    def update_temperatures(self, t):
        self.current_temp = self.t_mean + self.t_amp * \
            math.cos(2 * math.pi / 24 * (t - self.t_peak))
        for item in self.items:
            item.update_temperature(t)

    # 2.12 code ref
    def __str__(self):
        return f"{self.block_type} Block {self.block_number}: topleft={self.topleft}, items={len(self.items)}, temp={self.current_temp:.1f}°C"
