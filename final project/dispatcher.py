
import matplotlib.pyplot as plt
from diagram_types import rear_end, left_turn, right_angle, head_on, side_swipe

def draw_crash_diagram(unit1_dir, unit1_mov, unit2_dir, unit2_mov, unit_at_fault, crash_type):
    fig, ax = plt.subplots(figsize=(6, 6))
    if crash_type == 'rear end':
        if unit1_mov == 'TH':
            rear_end.draw_straight_rear_end(ax, unit1_dir, 'red' if unit_at_fault == 'unit1' else 'limegreen',
                                                   'red' if unit_at_fault == 'unit2' else 'limegreen')
        else:
            rear_end.draw_curved_rear_end(ax, unit1_dir, unit1_mov,
                                                   'red' if unit_at_fault == 'unit1' else 'limegreen',
                                                   'red' if unit_at_fault == 'unit2' else 'limegreen')
    elif crash_type == 'left turn':
        left_turn.draw_bezier_LT(ax, unit1_dir, unit2_dir, unit_at_fault)
    elif crash_type == 'right angle':
        right_angle.draw_right_angle_diagram(unit1_dir, unit1_mov, unit2_dir, unit2_mov, unit_at_fault, ax)
    elif crash_type == 'head on':
        head_on.draw_head_on_diagram(unit1_dir, unit1_mov, unit2_dir, unit2_mov, unit_at_fault, ax)
    elif crash_type == 'side swipe':
        side_swipe.draw_side_swipe_diagram(unit1_dir, unit1_mov, unit2_dir, unit2_mov, unit_at_fault, ax)
    else:
        raise ValueError(f"Unknown crash type: {crash_type}")

    ax.set_xlim(0, 8)
    ax.set_ylim(0, 8)
    ax.set_aspect('equal')
    ax.axis('off')
    plt.show()
