from envs.robot_arm_env import RobotArmEnvironment
from utils.metrics import EpisodeMetrics
from utils.scenario_generator import ScenarioGenerator
# state -> action -> env -> reward -> next state
def main():
    print("Starting Robot Arm RL Project...")
    #scenario configuration
    scenario_generator = ScenarioGenerator(seed=42)
    scenario = scenario_generator.generate_random_scenario(number_of_obstacles=2)
    scenario_generator.print_scenario(scenario)
    
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

    metrics = EpisodeMetrics()

    # baseline test
    for step in range(100):
        action = robot_env.sample_action()

        observation, reward, done, terminated, truncated, info = robot_env.step(action)
        metrics.update(reward, action)
        print(f"Step {step + 1}: reward={reward:.4f}, done={done}")

        if done:
            break
    metrics.finish(observation, info)
    print("\nEpisode metrics:")
    for key, value in metrics.as_dict().items():
        print(f"{key}: {value}")
    robot_env.close()


if __name__ == "__main__":
    main()