from abc import ABC, abstractmethod

class BaseTool(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        pass

    @abstractmethod
    def get_definition(self):
        pass