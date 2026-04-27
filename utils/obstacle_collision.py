import numpy as np


def calculate_distance(point_a, point_b):
    """
    Euclidean distance between two 3D points.
    """
    return np.linalg.norm(point_a - point_b)


def check_object_obstacle_collision(object_position, obstacles, collision_threshold=0.07):
    """
    checks whether the object is too close to any obstacle.
    logical collision check.
    allows to valuate whether the task violates obstacle constraints.
    """
    collision_detected = False
    min_distance = None

    for obstacle in obstacles:
        obstacle_position = obstacle["position"]
        distance = calculate_distance(object_position, obstacle_position)

        if min_distance is None or distance < min_distance:
            min_distance = distance
        if distance < collision_threshold:
            collision_detected = True
    return collision_detected, min_distance