def inspect_mujoco_env(env):
    """
    available MuJoCo-related attributes.
    helps understand how to access the underlying simulation.
    """

    print("\nMuJoCo environment inspection:")

    current = env
    level = 0

    while hasattr(current, "env"):
        print(f"Level {level}: {type(current)}")
        current = current.env
        level += 1

    print(f"Final unwrapped env: {type(current)}")

    possible_attrs = [
        "model",
        "data",
        "sim",
        "mujoco_renderer",
        "robot",
        "goal",
        "initial_qpos",
    ]

    for attr in possible_attrs:
        print(f"has {attr}: {hasattr(current, attr)}")

    if hasattr(current, "model"):
        print("model available")
        print("number of bodies:", current.model.nbody)
        print("number of geoms:", current.model.ngeom)

    if hasattr(current, "data"):
        print("data available")

        if hasattr(current, "model"):
            print("\nBodies:")
            for i in range(current.model.nbody):
                print(i, current.model.body(i).name)

            print("\nGeoms:")
            for i in range(current.model.ngeom):
                print(i, current.model.geom(i).name)