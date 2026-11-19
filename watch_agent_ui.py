"""Xem agent chạy trên FrozenLake với giao diện đồ hoạ (pygame)."""
import time
from pathlib import Path

import gymnasium as gym
import numpy as np

POLICY_FILE = Path("policy.npy")
N_EPISODES = 5
STEPS_PER_SECOND = 3
RESULT_DELAY_SEC = 1.0


def load_policy(n_states, n_actions):
    """Lấy policy đã học nếu có, không thì dùng policy ngẫu nhiên."""
    if POLICY_FILE.exists():
        return np.load(POLICY_FILE), "policy đã học"
    return np.random.randint(0, n_actions, n_states), "policy NGẪU NHIÊN"


def run_episode(env, policy):
    """Chạy 1 episode, cửa sổ tự vẽ mỗi bước. Trả về (thắng?, số bước)."""
    state, _ = env.reset()
    steps = 0
    done = False
    reward = 0
    while not done:
        state, reward, terminated, truncated, _ = env.step(int(policy[state]))
        done = terminated or truncated
        steps += 1
    return reward == 1, steps


def main():
    env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=True, render_mode="human")
    env.unwrapped.metadata["render_fps"] = STEPS_PER_SECOND
    policy, policy_name = load_policy(env.observation_space.n, env.action_space.n)
    print(f"Đang dùng: {policy_name}")

    wins = 0
    for episode in range(1, N_EPISODES + 1):
        won, steps = run_episode(env, policy)
        wins += won
        result = "THẮNG" if won else "THUA"
        print(f"Episode {episode}/{N_EPISODES}: {result} ({steps} bước)")
        time.sleep(RESULT_DELAY_SEC)

    print(f"\nKết quả: thắng {wins}/{N_EPISODES} episode")
    env.close()


if __name__ == "__main__":
    main()