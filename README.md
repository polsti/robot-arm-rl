# Robot Arm Control via Reinforcement Learning

## Project Description
This project focuses on developing an intelligent robotic arm system using reinforcement learning.

The goal is to simulate a robotic arm that can:
- reach an object
- grasp it
- move it to a target location
- avoid obstacles
- optimize performance (time, movement efficiency, success rate)

The system is built using Gymnasium Robotics (FetchPickAndPlace environment).

## Team Members
- Polina - Environment & Simulation
- Dainius - RL Algorithm & Training
- Rustam - Integration & Documentation

## Current Environment Features
- Custom FetchPickAndPlace environment (PhysicalFetchPickAndPlaceDense-v0)
- Physical obstacles added directly into the MuJoCo XML model
- Scenario generation with object, target, and obstacle positions
- Scenario validation checks
- Multiple scenario evaluation
- Episode metrics
- Movement metrics
- Obstacle-aware metrics
- Collision-based reward penalty

## Setup Instructions
```bash
python3 -m venv robot_env
source robot_env/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python src/main.py
```

## Documentation
docs/environment.md
