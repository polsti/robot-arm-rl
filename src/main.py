from envs.robot_arm_env import RobotArmEnvironment


def main():
    print("Starting Robot Arm RL Project...")

    robot_env = RobotArmEnvironment(
        env_name="FetchPickAndPlaceDense-v4",
        render_mode="human"
    )

    env = robot_env.setup()
    # Reset environment (start new episode)
    observation, info = robot_env.reset(seed=42)

    print("Environment loaded successfully.")
    print("Observation keys:", observation.keys())
    print("Observation vector shape:", observation["observation"].shape)
    print("Achieved goal shape:", observation["achieved_goal"].shape)
    print("Desired goal shape:", observation["desired_goal"].shape)
    print("Action space:", env.action_space)
    # baseline test
    for step in range(100):
        action = robot_env.sample_action()

        observation, reward, done, terminated, truncated, info = robot_env.step(action)

        print(f"Step {step + 1}: reward={reward:.4f}, done={done}")

        if done:
            break

    robot_env.close()


if __name__ == "__main__":
    main()