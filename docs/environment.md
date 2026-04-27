# Environment & Simulation

## Overview

This module is responsible for generating and evaluating robotic manipulation scenarios.

The system simulates tasks where a robotic arm must:
- move an object (cube)
- reach a target position
- avoid obstacles
- optimize performance metrics

---

## Scenario Structure

Each scenario consists of three main components:

### 1. Object
The object represents the item the robot must manipulate.

```python
{
    "name": "cube_to_move",
    "position": [x, y, z],
    "size": [0.04, 0.04, 0.04]
}
```

### 2. Target
The target defines where the object should be placed.
```python
{
    "position": [x, y, z]
}
```

### 3. Obstacles
Obstacles are additional objects that increase task difficulty.

```python
[
    {
        "name": "obstacle_1",
        "position": [...],
        "size": [...]
    }
]
```
### 4. Scenario Generation 
Scenarios are generated randomly using ScenarioGenerator.
Key properties:
- random positions
- configurable number of obstacles
- reproducibility via seeds

scenario = generator.generate_random_scenario()


### 5. Scenario Validation

Generated scenarios are validated to ensure feasibility.

Validation rules:

object and target must not overlap
obstacles must not be too close to object
obstacles must not block the target

valid : True/False

### 6. Episode metrics
Each episode collects performance metrics:

total reward
number of steps
final distance to target
success flag

### 7. Movement Metrics
total action magnitude
average action magnitude
max action magnitude

These measure how efficiently the robot moves.

### 8. Obstacle-aware Metrics

Additional metrics describe scenario difficulty:

obstacle count
minimum object-obstacle distance
minimum target-obstacle distance

These help analyze how obstacle placement affects performance.

### Limitations
obstacles are not yet physically integrated into MuJoCo simulation
agent uses random actions (no training yet)
scenarios affect evaluation but not environment physics

### future steps ? 
integrate obstacles into simulation environment
connect scenario generator with MuJoCo scene
replace random policy with RL agent