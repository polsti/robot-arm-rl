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

        self.total_action_magnitude = 0.0
        self.max_action_magnitude = 0.0
        self.average_action_magnitude = 0.0

    def update(self, reward, action):
        """Updates reward and step counter after each environment step."""
        self.total_reward += reward
        self.steps += 1
        if action is not None:
            action_magnitude = np.linalg.norm(action)

            self.total_action_magnitude += action_magnitude
            self.max_action_magnitude = max(self.max_action_magnitude, action_magnitude)

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
        if self.steps > 0:
            self.average_action_magnitude = self.total_action_magnitude / self.steps
            
    def as_dict(self):
        """Returns metrics in dictionary format for printing or saving."""
        return {
            "total_reward": self.total_reward,
            "steps": self.steps,
            "final_distance": self.final_distance,
            "success": self.success,
            "total_action_magnitude": self.total_action_magnitude,
            "average_action_magnitude": self.average_action_magnitude,
            "max_action_magnitude": self.max_action_magnitude,
        }