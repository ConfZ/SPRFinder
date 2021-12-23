from mutator import Mutator
import numpy as np
import settings
import random
from dtw.dtw import dtw

class Thompson(Mutator):
    def __init__(self, ops):
        super().__init__()
        self.nIter = 0
        self.ops = ops
        self.nActions = len(self.ops)
        self.k = 1
        self.empiricalMeans = np.zeros(len(self.ops))
        self.lastAction = -1
        self.alphaBetaPairs = []
        for i in range(self.nActions):
            self.alphaBetaPairs.append([1, 1])
        self.time_list = [0, 0, 0]

    def __name__(self):
        return "thomp"

    def time_reward(self, times):
        self.time_list = times

    def random_select(self, banned_action):
        cand_act = list(set(self.ops) - set(banned_action))
        return random.choice(cand_act)

    def select_action(self, banned_actions=[]):
        R = np.zeros([self.nActions, self.k])
        for a in range(self.nActions):
            for i in range(self.k):
                R[a][i] = np.random.beta(self.alphaBetaPairs[a][0], self.alphaBetaPairs[a][1])
        for a in range(self.nActions):
            sum = 0.0
            for i in range(self.k):
                sum += R[a][i]
            self.empiricalMeans[a] = self.k * sum

        self.lastAction = -1
        val = np.NINF
        for a in range(self.nActions):
            if self.ops[a] in banned_actions:
                continue
            if self.empiricalMeans[a] > val:
                self.lastAction, val = a, self.empiricalMeans[a]


        return self.ops[self.lastAction]

    def init_mutation(self):
        self.empiricalMeans = np.zeros(len(self.ops))
        for i in range(self.nActions):
            self.alphaBetaPairs.append([1, 1])

    def get_time_similarity(self, times):
        return min([dtw(times, tl).distance for tl in settings.found_time_list])
    def reward(self, rew):
        rewardVal = None
        similarity = self.get_time_similarity(self.time_list)
        if rew:
            if len(settings.found_time_list) == 0:
                self.alphaBetaPairs[self.lastAction][0] += 1
            else:
                self.alphaBetaPairs[self.lastAction][0] += 0.8 + 0.01 * similarity
            target_op = self.ops[self.lastAction]
            if target_op in settings.op_dict:
                settings.op_dict[target_op] += 1
            else:
                settings.op_dict[target_op] = 1
            rewardVal = 1.0
        else:
            self.alphaBetaPairs[self.lastAction][1] += 1
            target_op = self.ops[self.lastAction]
            if target_op in settings.op_dict:
                if settings.op_dict[target_op] >= 1:
                    settings.op_dict[target_op] -= 1
            else:
                settings.op_dict[target_op] = 0
            rewardVal = 0.0
        self.nIter += 1
