from envs.robot_arm_env import RobotArmEnvironment

def main():
    print("Starting Robot Arm RL Project...")
    
    # Create environment
    robot_env = RobotArmEnvironment()
    env = robot_env.setup()
    
    # Test it
    obs = robot_env.reset()
    print(f"Environment loaded! Observation shape: {obs.shape}")

if __name__ == "__main__":
    main()
