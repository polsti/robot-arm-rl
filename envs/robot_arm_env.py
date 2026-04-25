import gymnasium as gym

class RobotArmEnvironment:
    def __init__(self, env_name="FetchReach-v2"):
        self.env_name = env_name
        self.env = None
    
    def setup(self):
        self.env = gym.make(self.env_name)
        return self.env
    
    def reset(self):
        obs, info = self.env.reset()
        return obs
    
    def step(self, action):
        return self.env.step(action)
    
    def render(self):
        return self.env.render()
