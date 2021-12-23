from abc import ABCMeta, abstractmethod


class Mutator:
    def __init__(self):
        self.model_required = True

    @abstractmethod
    def mutate(self, instance):
        pass

    @abstractmethod
    def reward(self, rewardVal):
        pass

    @abstractmethod
    def write_model(self):
        pass

    @abstractmethod
    def read_model(self):
        pass
