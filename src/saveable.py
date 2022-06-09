from abc import ABC
from typing import Dict


class Saveable(ABC):
    @classmethod
    def from_json(cls, data: Dict) -> 'Saveable':
        """
        Return a saveable object from the given state information

        The default implementation assumes that there are only primitive types as information.
        If this is not the case for a Saveable class, that class should provide its own implementation
        """

        # noinspection PyArgumentList
        return cls(**data)

    def as_json(self) -> Dict:
        """
        Return the object's state information
        """

        raise NotImplementedError()

    @classmethod
    def load(cls, *args, **kwargs):
        """
        Load the object from it's state information
        """

        raise NotImplementedError()

    def save(self):
        """
        Save the object's state information
        """

        raise NotImplementedError()
