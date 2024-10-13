import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec
from matplotlib.animation import FuncAnimation
from utils import *

from cano import *


# 4.1 code ref
# Function 8: Generate RGB image
def generate_rgb_image(blocks, block_size, map_shape):
    grid = np.zeros(
        (map_shape[0]*block_size, map_shape[1]*block_size, 3), dtype=np.uint8)
    for block in blocks:
        cx_start, ry_start = block.topleft
        block_image = block.generate_rgb_view()
        grid[ry_start:ry_start+block_size,
             cx_start:cx_start+block_size] = block_image
    return grid


# 4.2 code ref
# Function 9: Generate thermal image
def generate_thermal_image(blocks, block_size, map_shape):
    grid = np.zeros(
        (map_shape[0]*block_size, map_shape[1]*block_size), dtype=np.float32)
    for block in blocks:
        cx_start, ry_start = block.topleft
        block_image = block.generate_thermal_view()
        grid[ry_start:ry_start+block_size,
             cx_start:cx_start+block_size] = block_image
    return grid


# 4.3 code ref
# Function 10: Update temperatures
def update_temperatures(blocks, time):
    for block in blocks:
        block.update_temperatures(time)


# 4.4 code ref
# Function 11: Generate and display views
def generate_and_display_views(blocks, block_size, map_shape, num_blocks, time):
    fig = plt.figure(figsize=(12, 6))
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0.03, 1], wspace=0.3)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[2])

    # RGB image
    rgb_image = generate_rgb_image(blocks, block_size, map_shape)
    ax1.imshow(rgb_image)
    ax1.set_title("RGB View", fontsize=12)

    # Thermal image
    thermal_image = generate_thermal_image(blocks, block_size, map_shape)
    im2 = ax2.imshow(thermal_image, cmap='Spectral_r', vmin=5, vmax=40)
    ax2.set_title(f"Thermal View at {time:.2f} hours", fontsize=12)

    # Colorbar (vertical)
    cbar_ax = fig.add_subplot(gs[1])
    cbar = fig.colorbar(im2, cax=cbar_ax, orientation='vertical',
                        ticks=np.linspace(5, 40, num=5))
    cbar.set_label('Temperature (°C)', fontsize=12)
    cbar.ax.yaxis.set_label_position('left')
    cbar.ax.tick_params(labelsize=8)

    fig.suptitle(f"Map with {num_blocks} blocks", fontsize=14)
    plt.savefig(f"./result/map_{time:.2f}h.png", dpi=300)
    plt.show()


# 4.5 code ref
# Function 13: Simulate thermal view over time using FuncAnimation
def animate_thermal_view_func(blocks, block_size, map_shape, num_blocks):
    fig = plt.figure(figsize=(12, 6))
    fig.suptitle(f"Thermal View Animation for {num_blocks} Blocks", fontsize=12)
    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 0.05, 1], wspace=0.3)

    # RGB View
    ax1 = fig.add_subplot(gs[0])
    rgb_image = generate_rgb_image(blocks, block_size, map_shape)
    ax1.imshow(rgb_image)
    ax1.set_title("RGB View", fontsize=8)
    ax1.axis('off')

    # Thermal View
    ax2 = fig.add_subplot(gs[2])
    thermal_image = generate_thermal_image(blocks, block_size, map_shape)
    im2 = ax2.imshow(thermal_image, cmap='Spectral_r', vmin=5, vmax=40)
    ax2.set_title("Thermal View", fontsize=8)
    ax2.axis('off')

    # Colorbar
    cbar_ax = fig.add_subplot(gs[1])
    cbar = fig.colorbar(im2, cax=cbar_ax, orientation='vertical',
                        ticks=np.linspace(5, 40, num=5))
    cbar.set_label('Temperature (°C)', fontsize=12)
    cbar.ax.yaxis.set_label_position('left')
    cbar.ax.tick_params(labelsize=8)

    temp_annotations = []
    for block in blocks:
        annotation = ax2.annotate(
            f"{block.current_temp:.1f}°C",
            xy=(block.topleft[0] + block.size // 2,
                block.topleft[1] + block.size // 2),
            xycoords='data',
            fontsize=12, color='black', ha='center', va='center'
        )
        temp_annotations.append(annotation)

    time_annotation = ax2.annotate(
        '', xy=(0.08, 0.9), xycoords='axes fraction', fontsize=8, color='black', ha='center')

    def update(frame):
        time = frame / 10
        update_temperatures(blocks, time)
        thermal_image = generate_thermal_image(blocks, block_size, map_shape)
        im2.set_array(thermal_image)

        for block, annotation in zip(blocks, temp_annotations):
            block.update_temperatures(time)
            annotation.set_text(f"{block.current_temp:.1f}°C")

        time_annotation.set_text(f"Time: {time:.2f}h")
        return im2, time_annotation, *temp_annotations

    anim = FuncAnimation(fig, update, frames=240, interval=60, blit=True)
    
    # Save the animation as a GIF file
    anim.save('./result/thermal_view_animation.gif', writer='pillow', fps=30)

    plt.tight_layout()
    plt.show()


# 4.6 code ref
# Function 14: Simulate thermal view over time using loop techniques
def animate_thermal_view_loop(blocks, block_size, map_shape, num_blocks):
    plt.ion()

    fig = plt.figure(figsize=(12, 6))
    fig.suptitle(f"Thermal View Animation for {
                 num_blocks} Blocks", fontsize=12)
    gs = plt.GridSpec(1, 3, width_ratios=[1, 0.05, 1], wspace=0.3)

    ax1 = fig.add_subplot(gs[0])
    rgb_image = generate_rgb_image(blocks, block_size, map_shape)
    ax1.imshow(rgb_image)
    ax1.set_title("RGB View", fontsize=8)
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[2])
    thermal_image = generate_thermal_image(blocks, block_size, map_shape)
    im2 = ax2.imshow(thermal_image, cmap='Spectral_r', vmin=5, vmax=40)
    ax2.set_title("Thermal View", fontsize=8)
    ax2.axis('off')

    cbar_ax = fig.add_subplot(gs[1])
    cbar = fig.colorbar(im2, cax=cbar_ax, orientation='vertical',
                        ticks=np.linspace(5, 40, num=5))
    cbar.set_label('Temperature (°C)', fontsize=12)
    cbar.ax.yaxis.set_label_position('left')
    cbar.ax.tick_params(labelsize=8)

    temp_annotations = []
    for block in blocks:
        annotation = ax2.annotate(
            f"{block.current_temp:.1f}°C",
            xy=(block.topleft[0] + block.size // 2,
                block.topleft[1] + block.size // 2),
            xycoords='data',
            fontsize=12, color='black', ha='center', va='center'
        )
        temp_annotations.append(annotation)

    time_annotation = ax2.annotate(
        '', xy=(0.08, 0.9), xycoords='axes fraction', fontsize=8, color='black', ha='center')

    frame = 0
    while plt.fignum_exists(fig.number):
        plt.clf()
        gs = plt.GridSpec(1, 3, width_ratios=[1, 0.05, 1], wspace=0.3)

        fig.suptitle(f"Thermal View Animation for {
                     num_blocks} Blocks", fontsize=12)

        ax1 = fig.add_subplot(gs[0])
        rgb_image = generate_rgb_image(blocks, block_size, map_shape)
        ax1.imshow(rgb_image)
        ax1.set_title("RGB View", fontsize=8)
        ax1.axis('off')

        ax2 = fig.add_subplot(gs[2])
        thermal_image = generate_thermal_image(blocks, block_size, map_shape)
        im2 = ax2.imshow(thermal_image, cmap='Spectral_r', vmin=5, vmax=40)
        ax2.set_title("Thermal View", fontsize=8)
        ax2.axis('off')

        cbar_ax = fig.add_subplot(gs[1])
        cbar = fig.colorbar(
            im2, cax=cbar_ax, orientation='vertical', ticks=np.linspace(5, 40, num=5))
        cbar.set_label('Temperature (°C)', fontsize=12)
        cbar.ax.yaxis.set_label_position('left')
        cbar.ax.tick_params(labelsize=8)

        time = frame / 10
        update_temperatures(blocks, time)

        for block, annotation in zip(blocks, temp_annotations):
            block.update_temperatures(time)
            annotation.set_text(f"{block.current_temp:.1f}°C")
            ax2.annotate(
                f"{block.current_temp:.1f}°C",
                xy=(block.topleft[0] + block.size // 2,
                    block.topleft[1] + block.size // 2),
                xycoords='data',
                fontsize=12, color='black', ha='center', va='center'
            )

        time_annotation.set_text(f"Time: {time:.2f}h")
        ax2.annotate(
            f"Time: {time:.2f}h",
            xy=(0.08, 0.9), xycoords='axes fraction', fontsize=8, color='black', ha='center'
        )

        plt.tight_layout()
        plt.pause(0.1)

        frame += 1

    plt.ioff()
    plt.show()
