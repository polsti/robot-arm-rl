import os
import matplotlib.pyplot as plt


def visualize_scenario(scenario, save_path=None, show=False):
    """
    Creates a top-down 2D visualization of the generated scenario.
    Obstacles now exist visually.
    """

    object_position = scenario["object"]["position"]
    target_position = scenario["target"]["position"]
    obstacles = scenario["obstacles"]

    plt.figure(figsize=(7, 6))

    # Object
    plt.scatter(
        object_position[0],
        object_position[1],
        marker="s",
        s=180,
        label="Object / cube"
    )
    plt.text(
        object_position[0],
        object_position[1],
        " object",
        fontsize=9
    )

    # Target
    plt.scatter(
        target_position[0],
        target_position[1],
        marker="*",
        s=250,
        label="Target"
    )
    plt.text(
        target_position[0],
        target_position[1],
        " target",
        fontsize=9
    )

    # Obstacles
    for obstacle in obstacles:
        obstacle_position = obstacle["position"]

        plt.scatter(
            obstacle_position[0],
            obstacle_position[1],
            marker="X",
            s=220,
            label="Obstacle" if obstacle["name"] == "obstacle_1" else None
        )

        plt.text(
            obstacle_position[0],
            obstacle_position[1],
            f" {obstacle['name']}",
            fontsize=9
        )

    plt.title("Generated Scenario: Object, Target, and Obstacles")
    plt.xlabel("X position")
    plt.ylabel("Y position")

    # Workspace boundaries used in ScenarioGenerator
    plt.xlim(1.10, 1.55)
    plt.ylim(0.50, 1.00)

    plt.grid(True)
    plt.legend()
    plt.gca().set_aspect("equal", adjustable="box")

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, bbox_inches="tight")
        print(f"Scenario visualization saved to: {save_path}")

    if show:
        plt.show()

    plt.close()