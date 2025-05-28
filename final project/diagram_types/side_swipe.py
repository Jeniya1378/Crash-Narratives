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

direction_angle = {'NB': 90, 'SB': 270, 'EB': 0, 'WB': 180}

def rotate_vector(vec, angle_deg):
    angle_rad = np.radians(angle_deg)
    x, y = vec
    x_new = x * np.cos(angle_rad) - y * np.sin(angle_rad)
    y_new = x * np.sin(angle_rad) + y * np.cos(angle_rad)
    return x_new, y_new

def draw_unit_to_point_side_swipe(ax, tip_x, tip_y, direction, movement, color, length=1.5):
    dx, dy = movement_vector.get((direction, movement), (0, 1))
    dx *= length
    dy *= length
    ax.arrow(tip_x - dx, tip_y - dy, dx, dy, head_width=0.2, head_length=0.2,
             fc=color, ec=color, linewidth=2, length_includes_head=True)

def draw_side_swipe_arrow_to_point(ax, tip_x, tip_y, direction, color, lane_offset=0.6, total_length=1.5):
    forward_vec = rotate_vector((0, 1), direction_angle[direction])
    side_vec = rotate_vector((1, 0), direction_angle[direction])
    dx2 = (forward_vec[0] + side_vec[0]) * (lane_offset / 1.414)
    dy2 = (forward_vec[1] + side_vec[1]) * (lane_offset / 1.414)
    x_corner = tip_x - dx2
    y_corner = tip_y - dy2
    straight_length = total_length - (lane_offset / 1.414)
    x_start = x_corner - forward_vec[0] * straight_length
    y_start = y_corner - forward_vec[1] * straight_length
    ax.plot([x_start, x_corner], [y_start, y_corner], color=color, linewidth=2)
    ax.arrow(x_corner, y_corner, dx2, dy2, head_width=0.2, head_length=0.2,
             fc=color, ec=color, linewidth=2, length_includes_head=True)





def draw_side_swipe_diagram(unit1_dir, unit1_mov, unit2_dir, unit2_mov, unit_at_fault, ax):
    base_x, base_y = 4, 4
    unit1_color = 'red' if unit_at_fault.lower() == 'unit1' else 'limegreen'
    unit2_color = 'red' if unit_at_fault.lower() == 'unit2' else 'limegreen'

    lane_offset = 0.6
    arrow_length = 1.5

    if unit1_dir in ['EB', 'WB']:
        tip_x, tip_y = base_x + 2, base_y
    elif unit1_dir in ['NB', 'SB']:
        tip_x, tip_y = base_x, base_y + 2
    else:
        return

    draw_unit_to_point_side_swipe(ax, tip_x, tip_y, unit2_dir, unit2_mov, unit2_color, arrow_length)
    draw_side_swipe_arrow_to_point(ax, tip_x, tip_y, unit1_dir, unit1_color, lane_offset, total_length=arrow_length)

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'{unit1_dir}-{unit1_mov} vs {unit2_dir}-{unit2_mov}', fontsize=8)

# # Grid visualization (commented out for production use)
# directions = ['NB', 'SB', 'EB', 'WB']
# movements = ['TH', 'LT', 'RT']
# fig, axs = plt.subplots(4, 3, figsize=(12, 16))
# axs = axs.flatten()
# index = 0

# for dir in directions:
#     for mov in movements:
#         ax = axs[index]
#         draw_side_swipe_diagram(dir, mov, dir, mov, 'unit1', ax)
#         index += 1

# plt.tight_layout()
# plt.show()