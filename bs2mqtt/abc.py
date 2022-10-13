import abc

class ICommmand(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def execute(self, options):
        raise NotImplementedError()
