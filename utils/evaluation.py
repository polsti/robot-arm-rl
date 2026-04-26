from utils.metrics import EpisodeMetrics
from utils.scenario_generator import ScenarioGenerator
import numpy as np

def run_single_episode(robot_env, scenario_seed, number_of_obstacles=2, max_steps=100):
    """
    Runs one episode and returns scenario data together with episode metrics.
    At this stage, the scenario is used for configuration/logging.
    no MuJoCo yet
    """
    scenario_generator = ScenarioGenerator(seed=scenario_seed)
    scenario = scenario_generator.generate_random_scenario(
        number_of_obstacles=number_of_obstacles
    )

    observation, info = robot_env.reset(seed=scenario_seed)
    metrics = EpisodeMetrics()

    for _ in range(max_steps):
        action = robot_env.sample_action()
        observation, reward, done, terminated, truncated, info = robot_env.step(action)
        metrics.update(reward, action)
        if done: break

    metrics.finish(observation, info)
    obstacle_metrics = calculate_obstacle_metrics(scenario)
    episode_metrics = metrics.as_dict()
    episode_metrics.update(obstacle_metrics)
    return {
        "scenario_seed": scenario_seed,
        "scenario": scenario,
        "metrics": episode_metrics,
    }

def run_multiple_scenarios(
    robot_env,
    number_of_scenarios=3,
    number_of_obstacles=2,
    max_steps=100,
):
    """
    Runs several episodes with different scenario seeds.
    """
    results = []
    for scenario_id in range(number_of_scenarios):
        scenario_seed = 42 + scenario_id

        result = run_single_episode(
            robot_env=robot_env,
            scenario_seed=scenario_seed,
            number_of_obstacles=number_of_obstacles,
            max_steps=max_steps,
        )
        result["scenario_id"] = scenario_id + 1
        results.append(result)

    return results

def calculate_obstacle_metrics(scenario):
    """C
    calculates obstacle-related metrics for a generated scenario.

    metrics describe how difficult or risky the scenario is:
    - how close the object is to obstacles
    - how close the target is to obstacles
    - how many obstacles are present
    """
    object_position = scenario["object"]["position"]
    target_position = scenario["target"]["position"]
    obstacles = scenario["obstacles"]

    if not obstacles:
        return {
            "obstacle_count": 0,
            "min_object_obstacle_distance": None,
            "min_target_obstacle_distance": None,
        }
    object_distances = []
    target_distances = []
    for obstacle in obstacles:
        obstacle_position = obstacle["position"]

        object_distance = np.linalg.norm(object_position - obstacle_position)
        target_distance = np.linalg.norm(target_position - obstacle_position)

        object_distances.append(object_distance)
        target_distances.append(target_distance)

    return {
        "obstacle_count": len(obstacles),
        "min_object_obstacle_distance": min(object_distances),
        "min_target_obstacle_distance": min(target_distances),
    }

def print_evaluation_results(results):
    print("\nMultiple scenario evaluation:")
    for result in results:
        metrics = result["metrics"]

        print(f"\nScenario {result['scenario_id']} | seed={result['scenario_seed']}")
        print(f"  total_reward: {metrics['total_reward']}")
        print(f"  steps: {metrics['steps']}")
        print(f"  final_distance: {metrics['final_distance']}")
        print(f"  success: {metrics['success']}")
        print(f"  total_action_magnitude: {metrics['total_action_magnitude']}")
        print(f"  average_action_magnitude: {metrics['average_action_magnitude']}")
        print(f"  max_action_magnitude: {metrics['max_action_magnitude']}")
        print(f"  obstacle_count: {metrics['obstacle_count']}")
        print(f"  min_object_obstacle_distance: {metrics['min_object_obstacle_distance']}")
        print(f"  min_target_obstacle_distance: {metrics['min_target_obstacle_distance']}")


def print_average_summary(results):
    """
    average metrics over all evaluated scenarios.
    """
    total_reward = 0.0
    final_distance = 0.0
    success_count = 0
    total_action_magnitude = 0.0
    average_action_magnitude = 0.0
    max_action_magnitude = 0.0
    min_object_obstacle_distance = 0.0
    min_target_obstacle_distance = 0.0

    for result in results:
        metrics = result["metrics"]
        total_reward += metrics["total_reward"]
        final_distance += metrics["final_distance"]
        success_count += int(metrics["success"])
        total_action_magnitude += metrics["total_action_magnitude"]
        average_action_magnitude += metrics["average_action_magnitude"]
        max_action_magnitude += metrics["max_action_magnitude"]
        min_object_obstacle_distance += metrics["min_object_obstacle_distance"]
        min_target_obstacle_distance += metrics["min_target_obstacle_distance"]

    n = len(results)
    print("\nAverage evaluation summary:")
    print(f"  average_total_reward: {total_reward / n}")
    print(f"  average_final_distance: {final_distance / n}")
    print(f"  success_rate: {success_count / n}")
    print(f"  average_total_action_magnitude: {total_action_magnitude / n}")
    print(f"  average_action_magnitude: {average_action_magnitude / n}")
    print(f"  average_max_action_magnitude: {max_action_magnitude / n}")
    print(f"  average_min_object_obstacle_distance: {min_object_obstacle_distance / n}")
    print(f"  average_min_target_obstacle_distance: {min_target_obstacle_distance / n}")