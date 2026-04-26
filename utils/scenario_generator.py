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
        # reacheble workspace
        self.x_range = (1.15, 1.50)
        self.y_range = (0.55, 0.95)
        self.z_table = 0.42
        # min allowed distance between objects 
        self.min_object_target_distance = 0.08
        self.min_obstacle_distance = 0.08

    def generate_fixed_scenario(self):
        """
        simple predefined scenario.
        useful for testing because the scenario is always the same.
        """
        scenario = {
            "object": {
                "name": "cube_to_move",
                "position": np.array([1.25, 0.75, self.z_table]),
                "size": np.array([0.04, 0.04, 0.04]),
            },
            "target": {
                "position": np.array([1.40, 0.90, self.z_table]),
            },
            "obstacles": [
                {
                    "name": "obstacle_1",
                    "position": np.array([1.32, 0.82, self.z_table]),
                    "size": np.array([0.05, 0.05, 0.05]),
                }
            ],
        }

        return scenario

    def generate_random_scenario(self, number_of_obstacles=2, max_attempts=100):
        """
        random scenario.

        The object, target, and obstacles are generated inside an approximate
        reachable workspace of the Fetch robotic arm.
        """
        for attempt in range(max_attempts):
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

            if self.is_valid_scenario(scenario):
                return scenario

        raise RuntimeError("Could not generate a valid scenario. Try reducing obstacles or changing ranges.")
    
    def is_valid_scenario(self, scenario):
        """
        valid scenario means:
        - object and target are not too close
        - obstacles are not too close to object
        - obstacles are not too close to target
        - obstacles are not too close to each other
        - all positions are inside workspace
        """
        object_position = scenario["object"]["position"]
        target_position = scenario["target"]["position"]
        obstacles = scenario["obstacles"]

        if not self._is_inside_workspace(object_position):
            return False

        if not self._is_inside_workspace(target_position):
            return False

        object_target_distance = self._distance(object_position, target_position)
        if object_target_distance < self.min_object_target_distance:
            return False

        for obstacle in obstacles:
            obstacle_position = obstacle["position"]

            if not self._is_inside_workspace(obstacle_position):
                return False

            if self._distance(object_position, obstacle_position) < self.min_obstacle_distance:
                return False

            if self._distance(target_position, obstacle_position) < self.min_obstacle_distance:
                return False

        for i in range(len(obstacles)):
            for j in range(i + 1, len(obstacles)):
                pos_i = obstacles[i]["position"]
                pos_j = obstacles[j]["position"]

                if self._distance(pos_i, pos_j) < self.min_obstacle_distance:
                    return False
        return True

    def _random_position(self):
        """
        random 3D position on the table.
        """
        x = self.rng.uniform(self.x_range[0], self.x_range[1])
        y = self.rng.uniform(self.y_range[0], self.y_range[1])
        z = self.z_table

        return np.array([x, y, z])

    def _distance(self, positions_a, positions_b):
        # Euclidean distance between two 3D positions.
        return np.linalg.norm(positions_a - positions_b)

    def _is_inside_workspace(self, position):
        x, y, z = position
        return (
            self.x_range[0] <= x <= self.x_range[1]
            and self.y_range[0] <= y <= self.y_range[1]
            and z == self.z_table
        )

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
        print("\nValidation:")
        print(f"  valid scenario: {self.is_valid_scenario(scenario)}")