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

## Setup Instructions
```bash
python3 -m venv robot_env
source robot_env/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python src/main.py
```

## Documentation
docs/environment.md
