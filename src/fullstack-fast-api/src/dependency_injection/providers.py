from typing import TypeVar
from enum import Enum


class DependencyType(Enum):
    TRANSIENT = 1
    SINGLETON = 2


class ServiceContainer:
    __dependencies = dict()

    T = TypeVar("T")

    @classmethod
    def register(cls, interface: T, service: T,
                 dependency_type: DependencyType = DependencyType.SINGLETON,
                 **service_kwargs):
        if '__init__' in service.__dict__:
            for arg_name, arg_type in service.__init__.__annotations__.items():
                if arg_name not in service_kwargs:
                    service_kwargs[arg_name] = cls.get(arg_type)

        match dependency_type:
            case DependencyType.SINGLETON:
                cls.__dependencies[interface.__name__] = (dependency_type, service(**service_kwargs))
            case DependencyType.TRANSIENT:
                cls.__dependencies[interface.__name__] = (dependency_type, (service, service_kwargs))

        return cls

    @classmethod
    def unregister(cls, interface):
        if interface.__name__ in cls.__dependencies:
            del cls.__dependencies[interface.__name__]

        return cls

    @classmethod
    def get(cls, interface: T) -> T:
        match cls.__dependencies[interface.__name__][0]:
            case DependencyType.SINGLETON:
                return cls.__dependencies[interface.__name__][1]
            case DependencyType.TRANSIENT:
                service = cls.__dependencies[interface.__name__][1][0]
                service_kwargs = cls.__dependencies[interface.__name__][1][1]
                return service(**service_kwargs)
