import random
import pandas as pd

from gym import Env
from gym.spaces import Discrete, Box
import numpy as np

class Market(Env):
    def __init__(self, df, window):
        self.df = df
        self.window = window

        self.shape = df.shape
        self.actions = Discrete(3)

        self.state = self.df[:self.window]
        self.observation_space = Box(low=-np.inf, high=np.inf, shape=self.shape, dtype=np.float64)

        self._runs = 0
        self._bought_at = 0
        self._total_reward = 0

    def step(self, action):
        done = False

        action -= 1

        self._runs += 1
        self.reward = 0

        self.close = self.state['close'].tolist()

        if action == 1 and self._bought_at > 0:
            self.reward += -0.1
        if action == 1 and self._bought_at == 0:
            self._bought_at = self.close[-1]


        if action == -1 and self._bought_at == 0:
            self.reward += -0.1
        if action == -1 and self._bought_at > 0:

            self.reward = ( (self.close[-1] - self._bought_at) / self._bought_at) * 100
            self._bought_at = 0

        if len(self.df) - 1 > self.window + self._runs:

            done = False
            self.state = self.df[self._runs : self.window + self._runs]


        if len(self.df) <= self.window + self._runs:
            done = True

        self._total_reward += self.reward

        info = dict(
            reward = self.reward,
            total_reward = self._total_reward,
            run = self._runs,
            position = action,
        )

        return self.state, self.reward, done, info

    def reset(self):
        self.state = self.df[:self.window]
        self._runs = 0
        self._bought_at = 0
        self._total_reward = 0

        return self.state

opens = list(range(1000))
closes = list(range(2000, 3000))
highs = list(range(3000, 4000))
lows = list(range(4000, 5000))

for i in range(5):
    random.shuffle(opens)
    random.shuffle(closes)
    random.shuffle(highs)
    random.shuffle(lows)

df = pd.DataFrame({
    'open': opens,
    'close': closes,
    'high': highs,
    'lows': lows
    })

env = Market(df, 5)

for i in range(100):
    state = env.reset()
    done = False   

    while not done:
        action = env.actions.sample()
        state, reward, done, info = env.step(action)
    
    print('Episode: {} Score: {}'.format(i+1, env._total_reward))
