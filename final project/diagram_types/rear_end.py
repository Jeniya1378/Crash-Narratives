import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Movement vectors for straight motion
movement_vector = {
    'NB': (0, 1),
    'SB': (0, -1),
    'EB': (1, 0),
    'WB': (-1, 0)
}

# Function to draw a straight rear-end crash (TH)
def draw_straight_rear_end(ax, direction, unit1_color, unit2_color):
    dx, dy = movement_vector[direction]
    offset = 1.5
    base_x, base_y = 4, 4
    base1_x = base_x - dx * offset
    base1_y = base_y - dy * offset

    # Arrow for unit1
    tip1_x = base1_x + dx * 1.5
    tip1_y = base1_y + dy * 1.5
    ax.arrow(base1_x, base1_y, dx * 1.5, dy * 1.5, head_width=0.2, head_length=0.3,
             fc=unit1_color, ec=unit1_color, linewidth=2, length_includes_head=True)

    # Arrow for unit2
    ax.arrow(tip1_x, tip1_y, dx * 1.5, dy * 1.5, head_width=0.2, head_length=0.3,
             fc=unit2_color, ec=unit2_color, linewidth=2, length_includes_head=True)

# Function to draw a curved rear-end crash (LT, RT)
def draw_curved_rear_end(ax, direction, movement, unit1_color, unit2_color):
    radius = 1.2
    center = {
        ('NB', 'LT'): (2.8, 5.2), ('SB', 'LT'): (5.2, 2.8),
        ('EB', 'LT'): (2.8, 2.8), ('WB', 'LT'): (5.2, 5.2),
        ('NB', 'RT'): (2.8, 2.8), ('SB', 'RT'): (5.2, 5.2),
        ('EB', 'RT'): (2.8, 5.2), ('WB', 'RT'): (5.2, 2.8)
    }[(direction, movement)]
    theta_ranges = {
        ('NB', 'LT'): (270, 360), ('SB', 'LT'): (90, 180),
        ('EB', 'LT'): (180, 270), ('WB', 'LT'): (0, 90),
        ('NB', 'RT'): (180, 270), ('SB', 'RT'): (0, 90),
        ('EB', 'RT'): (270, 360), ('WB', 'RT'): (90, 180)
    }
    theta1, theta2 = theta_ranges[(direction, movement)]

    # Unit2 (front)
    theta = np.radians(np.linspace(theta1, theta2, 100))
    x2 = center[0] + radius * np.cos(theta)
    y2 = center[1] + radius * np.sin(theta)
    ax.plot(x2, y2, color=unit2_color, linewidth=2)
    ax.arrow(x2[-2], y2[-2], x2[-1] - x2[-2], y2[-1] - y2[-2],
             head_width=0.2, head_length=0.2, fc=unit2_color, ec=unit2_color)

    # Unit1 (rear), slightly offset radius
    radius_1 = radius + 0.15
    x1 = center[0] + radius_1 * np.cos(theta)
    y1 = center[1] + radius_1 * np.sin(theta)
    ax.plot(x1, y1, color=unit1_color, linewidth=2)
    ax.arrow(x1[-2], y1[-2], x1[-1] - x1[-2], y1[-1] - y1[-2],
             head_width=0.2, head_length=0.2, fc=unit1_color, ec=unit1_color)

# # Main function to draw all 12 rear-end scenarios
# def draw_all_rear_end_crashes():
#     directions = ['NB', 'SB', 'EB', 'WB']
#     movements = ['TH', 'LT', 'RT']
#     fig, axes = plt.subplots(3, 4, figsize=(16, 10))
#     unit1_color = 'red'
#     unit2_color = 'limegreen'

#     for i, movement in enumerate(movements):
#         for j, direction in enumerate(directions):
#             ax = axes[i][j]
#             ax.set_xlim(0, 8)
#             ax.set_ylim(0, 8)
#             ax.set_aspect('equal')
#             ax.axis('off')
#             ax.set_title(f'{direction}-{movement}', fontsize=10)

#             if movement == 'TH':
#                 draw_straight_rear_end(ax, direction, unit1_color, unit2_color)
#             else:
#                 draw_curved_rear_end(ax, direction, movement, unit1_color, unit2_color)

#     plt.tight_layout()
#     plt.show()

# # Run the drawing
# draw_all_rear_end_crashes()
