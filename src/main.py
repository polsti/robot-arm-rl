from envs.robot_arm_env import RobotArmEnvironment
from utils.evaluation import (
    run_multiple_scenarios,
    print_evaluation_results,
    print_average_summary,
)
from utils.mujoco_debug import inspect_mujoco_env
def main():
    print("Starting Robot Arm RL Project...")

    robot_env = RobotArmEnvironment(
        env_name="FetchPickAndPlaceDense-v4",
        render_mode="human"
    )
    env = robot_env.setup()
    from utils.mujoco_debug import inspect_mujoco_env
    inspect_mujoco_env(env)

    print("\nEnvironment loaded successfully.")
    print("Action space:", env.action_space)
    print("Observation space:", env.observation_space)

    results = run_multiple_scenarios(
        robot_env=robot_env,
        number_of_scenarios=3,
        number_of_obstacles=2,
        max_steps=100,
        visualize=True,
    )
    print_evaluation_results(results)
    print_average_summary(results)
    robot_env.close()

if __name__ == "__main__":
    main()