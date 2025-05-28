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

def draw_arrow(ax, start, end, color):
    dx, dy = end[0] - start[0], end[1] - start[1]
    ax.arrow(start[0], start[1], dx, dy,
             head_width=0.1, head_length=0.2,
             fc=color, ec=color, linewidth=2, length_includes_head=True)

def draw_bezier_curve(ax, p0, p1, p2, color):
    t = np.linspace(0, 1, 100)
    x = (1 - t)**2 * p0[0] + 2 * (1 - t) * t * p1[0] + t**2 * p2[0]
    y = (1 - t)**2 * p0[1] + 2 * (1 - t) * t * p1[1] + t**2 * p2[1]

    ax.plot(x, y, color=color, linewidth=2)
    dx = x[-1] - x[-2]
    dy = y[-1] - y[-2]
    ax.arrow(x[-2], y[-2], dx, dy,
             head_width=0.1, head_length=0.2,
             fc=color, ec=color, length_includes_head=True)

def draw_bezier_LT(ax, unit1_dir, unit2_dir, unit_at_fault):
    # Define base position and curve control dynamically
    base = (4, 4)
    offset = 2
    ctrl_offset = 1.5
    crash_point = base

    lt_start = {
        'NB': (base[0], base[1] - offset),
        'SB': (base[0], base[1] + offset),
        'EB': (base[0] + offset, base[1]),
        'WB': (base[0] - offset, base[1])
    }[unit1_dir]

    control = {
        'NB': (base[0] - ctrl_offset, base[1] - ctrl_offset),
        'SB': (base[0] + ctrl_offset, base[1] + ctrl_offset),
        'EB': (base[0] + ctrl_offset, base[1] - ctrl_offset),
        'WB': (base[0] - ctrl_offset, base[1] + ctrl_offset)
    }[unit1_dir]

    through_start_vec = movement_vector[(unit2_dir, 'TH')]
    through_start = (base[0] - through_start_vec[0] * offset, base[1] - through_start_vec[1] * offset)

    unit1_color = 'red' if unit_at_fault.lower() == 'unit1' else 'limegreen'
    unit2_color = 'red' if unit_at_fault.lower() == 'unit2' else 'limegreen'

    draw_arrow(ax, through_start, crash_point, unit2_color)
    draw_bezier_curve(ax, lt_start, control, crash_point, unit1_color)

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(f'{unit1_dir}-LT vs {unit2_dir}-TH', fontsize=8)

# # Old grid visualization (commented out)
# fig, axes = plt.subplots(2, 2, figsize=(10, 10))
# directions = ['NB', 'SB', 'EB', 'WB']
# crash_point = (0, 0)

# for ax, direction in zip(axes.flat, directions):
#     ax.set_aspect('equal')
#     ax.set_xlim(-2, 2)
#     ax.set_ylim(-2, 2)
#     ax.axis('off')
#     ax.set_title(f'{direction} LT Crash', fontsize=12)

#     cfg = lt_configurations[direction]
#     draw_arrow(ax, cfg['through_start'], crash_point, 'lime')
#     draw_bezier_curve(ax, cfg['lt_start'], cfg['control'], crash_point, 'red')

# plt.tight_layout()
# plt.show()
