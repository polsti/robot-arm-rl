import numpy as np


class MujocoObstacleVisualizer:
    """
    scenario obstacles inside the MuJoCo viewer.
     obstacles are visual markers only.
    They are shown in the MuJoCo window but do not affect physics yet.
    """

    def __init__(self):
        self.warning_printed = False

    def draw_obstacles(self, env, scenario):
        """
        Draws obstacle markers in the MuJoCo viewer if the viewer supports markers.
        """

        viewer = self._get_viewer(env)
        if viewer is None:
            if not self.warning_printed:
                print("MuJoCo viewer is not available yet. Obstacles cannot be drawn.")
                self.warning_printed = True
            return

        for obstacle in scenario["obstacles"]:
            position = obstacle["position"]
            size = obstacle["size"]

            self._add_marker(
                viewer=viewer,
                position=position,
                size=size,
                label=obstacle["name"],
            )

    def _get_viewer(self, env):
        """
        tries to access the MuJoCo viewer from the wrapped Gymnasium environment.
        """

        unwrapped_env = env.unwrapped

        if not hasattr(unwrapped_env, "mujoco_renderer"):
            return None

        renderer = unwrapped_env.mujoco_renderer

        if not hasattr(renderer, "viewer"):
            return None

        return renderer.viewer

    def _add_marker(self, viewer, position, size, label):
        """
        visual marker to the MuJoCo viewer.
        marker is a red transparent box placed at the obstacle position.
        """

        if not hasattr(viewer, "add_marker"):
            if not self.warning_printed:
                print("This MuJoCo viewer does not support add_marker().")
                self.warning_printed = True
            return

        viewer.add_marker(
            pos=np.array(position),
            size=np.array(size),
            rgba=np.array([1.0, 0.0, 0.0, 0.6]),
            type=6,
            label=label,
        )