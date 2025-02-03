from abc import ABC, abstractmethod

class DiceRepository(ABC):

    @abstractmethod
    def rollDice(self):
        pass

