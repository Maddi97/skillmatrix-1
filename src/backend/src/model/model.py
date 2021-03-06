"""Contains the prototypical model with .to_json(self)"""
from abc import ABCMeta, abstractmethod


class Model(metaclass=ABCMeta):

    """Prototypical model"""
    @abstractmethod
    def jsonable(self):
        """Needs to be implemented by deriving classes, raises NotImplementedError otherwise."""
        raise NotImplementedError
