from abc import ABC, abstractmethod


class AccountRepository(ABC):

    @abstractmethod
    def save(self, email):
        pass