import os
import numpy as np
import mujoco
from gymnasium import utils
from gymnasium_robotics.envs.fetch.fetch_env import MujocoFetchEnv

class PhysicalObstacleFetchPickAndPlaceEnv(MujocoFetchEnv, utils.EzPickle):
    def __init__(self, reward_type="dense", **kwargs):
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        model_path = os.path.join(project_root,
                                  "assets",
                                  "fetch",
                                  "pick_and_place_obstacles.xml")

        with open("./target.txt", "r") as f:
            line = f.readline().strip()
            numbers = line.split(" ")
            x, y, z = np.array([float(x) for x in numbers])

        initial_qpos = {"robot0:slide0": 0.405,
                        "robot0:slide1": 0.48,
                        "robot0:slide2": 0.0,
                        "object0:joint": [x, y, z, 0.0, 0.0, 0.0, 0.0]}

        MujocoFetchEnv.__init__(self,
                                model_path=model_path,
                                has_object=True,
                                block_gripper=False,
                                n_substeps=20,
                                gripper_extra_height=0.2,
                                target_in_the_air=False,
                                target_offset=0.0,
                                obj_range=0.15,
                                target_range=0.15,
                                distance_threshold=0.05,
                                initial_qpos=initial_qpos,
                                reward_type=reward_type,
                                **kwargs)

        utils.EzPickle.__init__(self, reward_type=reward_type, **kwargs)

        with open("./goal.txt", "r") as f:
            line = f.readline().strip()
            numbers = line.split(" ")
            self.goal = np.array([float(x) for x in numbers])

    def _sample_goal(self):
        return self.goal

    def _reset_sim(self):
        super()._reset_sim()
        with open("./target.txt", "r") as f:
            line = f.readline().strip()
            numbers = line.split(" ")
            x, y, z = np.array([float(x) for x in numbers])

        with open("./goal.txt", "r") as f:
            line = f.readline().strip()
            numbers = line.split(" ")
            self.goal = np.array([float(x) for x in numbers])

        qpos = np.array([x, y, z, 1.0, 0.0, 0.0, 0.0], dtype=np.float64)

        joint = self.data.joint("object0:joint")
        joint.qpos[:] = qpos

        mujoco.mj_forward(self.model, self.data)
        return True