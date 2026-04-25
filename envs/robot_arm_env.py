import gymnasium as gym
import gymnasium_robotics


class RobotArmEnvironment:
    """
    Wrapper around Gymnasium-Robotics Fetch environments.

    This class abstracts interaction with the simulation:
    - creating the environment
    - resetting episodes
    - stepping through actions
    - rendering
    - closing

    Used by RL agent (later) to interact with the environment.
    """

    def __init__(self, env_name="FetchPickAndPlaceDense-v4", render_mode=None):
        self.env_name = env_name
        self.render_mode = render_mode
        self.env = None

    def setup(self):
        gym.register_envs(gymnasium_robotics)

        self.env = gym.make(
            self.env_name,
            render_mode=self.render_mode,
            max_episode_steps=100 # limit episode length
        )

        return self.env

    def reset(self, seed=None):
        """Reset the environment and return the initial observation and info.
        :return:
            observation: dict with keys:
                - observation (full state)
                - achieved_goal (current goal position)
                - desired_goal (target position)
            info: additional metadata
        """
        if self.env is None:
            raise RuntimeError("Environment is not created. Call setup() first.")

        observation, info = self.env.reset(seed=seed)
        return observation, info

    def step(self, action):
        if self.env is None:
            raise RuntimeError("Environment is not created. Call setup() first.")

        observation, reward, terminated, truncated, info = self.env.step(action)
        done = terminated or truncated

        return observation, reward, done, terminated, truncated, info

    def sample_action(self):
        if self.env is None:
            raise RuntimeError("Environment is not created. Call setup() first.")

        return self.env.action_space.sample()

    def render(self):
        if self.env is not None:
            return self.env.render()

    def close(self):
        if self.env is not None:
            self.env.close()