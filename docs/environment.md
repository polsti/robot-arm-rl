# Environment & Simulation

## Overview

This module is responsible for generating and evaluating robotic manipulation scenarios.

The system simulates tasks where a robotic arm must:
- move an object (cube)
- reach a target position
- avoid obstacles
- optimize performance metrics
environment is based on Gymnasium Robotics FetchPickAndPlace and MuJoCo.
Environment Type -> PhysicalFetchPickAndPlaceDense-v0 (envs/physical_fetch_env.py)
MuJoCo model -> assets/fetch/pick_and_place_obstacles.xml
---

## Scenario Structure

Each scenario consists of three main components:

###  Object
The object represents the item the robot must manipulate.

```python
{
    "name": "cube_to_move",
    "position": [x, y, z],
    "size": [0.04, 0.04, 0.04]
}
```

###  Target
The target defines where the object should be placed.
```python
{
    "position": [x, y, z]
}
```

###  Obstacles
Obstacles are additional objects that increase task difficulty.

```python
[
    {
        "name": "obstacle_1",
        "position": [x, y, z],
        "size": [0.05, 0.05, 0.05]
    }
]
```
###  Scenario Generation 
Scenarios are generated randomly using ScenarioGenerator.
Key properties:
- random positions
- configurable number of obstacles
- reproducibility via seeds

scenario = generator.generate_random_scenario(number_of_obstacles=2)


###  Scenario Validation

Generated scenarios are validated to ensure feasibility.

Validation rules:

object and target must not overlap
obstacles must not be too close to object
obstacles must not block the target

valid : True/False

### Physical obstacles in MuJoCo
assets/fetch/pick_and_place_obstacles.xml
<body name="obstacle_1" pos="1.22 0.75 0.425">
    <geom
        name="obstacle_1_geom"
        type="box"
        size="0.025 0.025 0.025"
        rgba="1 0 0 1"
        condim="3">
    </geom>
</body>
Required MuJoCo assets are stored in:
assets/stls/fetch
assets/textures
These files are needed because the custom XML references robot meshes and textures.

###  Episode metrics
Each episode collects performance metrics:

total reward
number of steps
final distance to target
success flag
These metrics are implemented in:
utils/metrics.py

###  Movement Metrics
total action magnitude
average action magnitude
max action magnitude

These measure how efficiently the robot moves.

###  Obstacle-aware Metrics

Additional metrics describe scenario difficulty:

obstacle count
minimum object-obstacle distance
minimum target-obstacle distance

These help analyze how obstacle placement affects performance.

### Collision Penalty
The evaluation logic includes a collision-based reward penalty.
If the object gets too close to an obstacle, the episode reward is reduced.
utils/obstacle_collision.py
utils/evaluation.py