import matplotlib.pyplot as plt
import numpy as np

movement_vector = {
    ('NB', 'TH'): (0, 1), ('SB', 'TH'): (0, -1),
    ('EB', 'TH'): (1, 0), ('WB', 'TH'): (-1, 0),
    ('NB', 'RT'): (1, 0), ('SB', 'RT'): (-1, 0),
    ('EB', 'RT'): (0, -1), ('WB', 'RT'): (0, 1),
    ('NB', 'LT'): (-1, 0), ('SB', 'LT'): (1, 0),
    ('EB', 'LT'): (0, 1), ('WB', 'LT'): (0, -1)
}

def draw_unit_to_point(ax, tip_x, tip_y, direction, movement, color, length=1.5):
    dx, dy = movement_vector.get((direction, movement), (0, 1))
    dx *= length
    dy *= length
    ax.arrow(tip_x - dx, tip_y - dy, dx, dy,
             head_width=0.2, head_length=0.2,
             fc=color, ec=color, linewidth=2,
             length_includes_head=True)

def draw_head_on_diagram(unit1_dir, unit1_mov, unit2_dir, unit2_mov, unit_at_fault, ax):
    base_x, base_y = 4, 4
    unit1_color = 'red' if unit_at_fault.lower() == 'unit1' else 'limegreen'
    unit2_color = 'red' if unit_at_fault.lower() == 'unit2' else 'limegreen'

    draw_unit_to_point(ax, base_x, base_y, unit1_dir, unit1_mov, unit1_color)
    draw_unit_to_point(ax, base_x, base_y, unit2_dir, unit2_mov, unit2_color)

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'{unit1_dir}-{unit1_mov} vs {unit2_dir}-{unit2_mov}', fontsize=8)

# # Old grid visualization (commented out)
# opposite_pairs = [('NB', 'SB'), ('SB', 'NB'), ('EB', 'WB'), ('WB', 'EB')]
# movements = ['TH', 'LT', 'RT']
# fig, axs = plt.subplots(len(opposite_pairs), len(movements), figsize=(12, 10))
# axs = axs.flatten()
# index = 0

# for dir1, dir2 in opposite_pairs:
#     for mov in movements:
#         ax = axs[index]
#         draw_head_on_diagram(dir1, mov, dir2, 'TH', 'unit1', ax)
#         index += 1

# plt.tight_layout()
# plt.show()
