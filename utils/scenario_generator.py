import numpy as np


class ScenarioGenerator:
    """
    A scenario describes:
    - object position
    - target position
    - obstacles

    This class does not directly modify the MuJoCo environment yet.
    It creates structured scenario data that can later be used by the environment.
    """

    def __init__(self, seed=None):
        """
        :param seed: random seed for reproducible scenario generation
        """
        self.rng = np.random.default_rng(seed)

    def generate_fixed_scenario(self):
        """
        simple predefined scenario.
        useful for testing because the scenario is always the same.
        """
        scenario = {
            "object": {
                "name": "cube_to_move",
                "position": np.array([1.25, 0.75, 0.42]),
                "size": np.array([0.04, 0.04, 0.04]),
            },
            "target": {
                "position": np.array([1.40, 0.90, 0.42]),
            },
            "obstacles": [
                {
                    "name": "obstacle_1",
                    "position": np.array([1.32, 0.82, 0.42]),
                    "size": np.array([0.05, 0.05, 0.05]),
                }
            ],
        }

        return scenario

    def generate_random_scenario(self, number_of_obstacles=2):
        """
        random scenario.

        The object, target, and obstacles are generated inside an approximate
        reachable workspace of the Fetch robotic arm.
        """
        object_position = self._random_position()
        target_position = self._random_position()

        obstacles = []

        for i in range(number_of_obstacles):
            obstacle = {
                "name": f"obstacle_{i + 1}",
                "position": self._random_position(),
                "size": np.array([0.05, 0.05, 0.05]),
            }
            obstacles.append(obstacle)

        scenario = {
            "object": {
                "name": "cube_to_move",
                "position": object_position,
                "size": np.array([0.04, 0.04, 0.04]),
            },
            "target": {
                "position": target_position,
            },
            "obstacles": obstacles,
        }

        return scenario

    def _random_position(self):
        """
        random 3D position on the table.

        Coordinates are chosen around the Fetch workspace.
        z is fixed because objects are placed on the table surface.
        """
        x = self.rng.uniform(1.15, 1.50)
        y = self.rng.uniform(0.55, 0.95)
        z = 0.42

        return np.array([x, y, z])

    def print_scenario(self, scenario):
        print("\nScenario configuration:")

        print("\nObject:")
        print(f"  name: {scenario['object']['name']}")
        print(f"  position: {scenario['object']['position']}")
        print(f"  size: {scenario['object']['size']}")

        print("\nTarget:")
        print(f"  position: {scenario['target']['position']}")

        print("\nObstacles:")
        if not scenario["obstacles"]:
            print("  no obstacles")
        else:
            for obstacle in scenario["obstacles"]:
                print(f"  name: {obstacle['name']}")
                print(f"  position: {obstacle['position']}")
                print(f"  size: {obstacle['size']}")