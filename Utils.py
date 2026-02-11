
# Utils.py

LANE_Y = 100 # Y coordinate of the player car (constant)

ROAD_PADDING = 140 # Padding to reduce the playable road width (increaes to narrow)

PHYSICAL_SIZE = { # Dimensions (width, height) for collision hitboxes
    "car": (60, 120),
    "bike": (35, 90),
    "car2": (60, 120),
    "truck": (90, 180)
}

VISUAL_SCALE = { # Scale factors for visual representation (unused with shapes)
    "car": 0.9,
    "bike": 0.6,
    "car2": 0.9,
    "truck": 1.2
}

def aabb(a, b): # Simple Axis-Aligned Bounding Box collision check
    ax, ay, aw, ah = a
    bx, by, bw, bh = b
    return (
        ax < bx + bw and
        ax + aw > bx and
        ay < by + bh and
        ay + ah > by
    )
