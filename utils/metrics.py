import numpy as np


class EpisodeMetrics:
    """
    Stores and calculates metrics for one episode.

    These metrics are useful for evaluating the agent:
    - total reward
    - number of steps
    - distance between achieved goal and desired goal
    - success flag
    """

    def __init__(self):
        self.total_reward = 0.0
        self.steps = 0
        self.final_distance = None
        self.success = False

    def update(self, reward):
        """Updates reward and step counter after each environment step."""
        self.total_reward += reward
        self.steps += 1

    def finish(self, observation, info):
        """
        Calculates final episode metrics.

        achieved_goal = current object position
        desired_goal = target object position
        distance = how far object is from the target
        """
        achieved_goal = observation["achieved_goal"]
        desired_goal = observation["desired_goal"]

        self.final_distance = np.linalg.norm(achieved_goal - desired_goal)

        # Gymnasium Robotics stores task success in info["is_success"]
        self.success = bool(info.get("is_success", False))

    def as_dict(self):
        """Returns metrics in dictionary format for printing or saving."""
        return {
            "total_reward": self.total_reward,
            "steps": self.steps,
            "final_distance": self.final_distance,
            "success": self.success,
        }