"""Xem agent chạy trên FrozenLake ngay trong terminal."""
import os
import time
from pathlib import Path

import gymnasium as gym
import numpy as np

POLICY_FILE = Path("policy.npy")
N_EPISODES = 3
STEP_DELAY_SEC = 0.5
RESULT_DELAY_SEC = 1.5


def load_policy(n_states, n_actions):
    """Lấy policy đã học nếu có, không thì dùng policy ngẫu nhiên."""
    if POLICY_FILE.exists():
        return np.load(POLICY_FILE), "policy đã học"
    return np.random.randint(0, n_actions, n_states), "policy NGẪU NHIÊN"


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def draw(env, header):
    clear_screen()
    print(header)
    print(env.render())


def run_episode(env, policy, header):
    """Chạy 1 episode, vẽ từng bước. Trả về (thắng?, số bước)."""
    state, _ = env.reset()
    steps = 0
    done = False
    reward = 0
    while not done:
        draw(env, f"{header} | bước {steps}")
        time.sleep(STEP_DELAY_SEC)
        state, reward, terminated, truncated, _ = env.step(int(policy[state]))
        done = terminated or truncated
        steps += 1
    draw(env, f"{header} | bước {steps}")
    return reward == 1, steps


def main():
    env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=True, render_mode="ansi")
    policy, policy_name = load_policy(env.observation_space.n, env.action_space.n)

    wins = 0
    for episode in range(1, N_EPISODES + 1):
        header = f"[{policy_name}] Episode {episode}/{N_EPISODES}"
        won, steps = run_episode(env, policy, header)
        wins += won
        print("THẮNG - tới G!" if won else "THUA - rơi xuống hố / hết bước", f"({steps} bước)")
        time.sleep(RESULT_DELAY_SEC)

    print(f"\nKết quả: thắng {wins}/{N_EPISODES} episode")
    env.close()


if __name__ == "__main__":
    main()