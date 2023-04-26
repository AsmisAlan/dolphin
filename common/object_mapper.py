from typing import Callable, Dict, Tuple, Type, TypeVar

TTarget = TypeVar("TTarget")
TSource = TypeVar("TSource")


class MappingAlreadyExistsException(Exception):
    """
    Exception raised when adding a new map for two classes that already exists.
    """


class MappingDoesNotExistException(Exception):
    """
    Exception raised during a mapping execution when a mapping does not exists.
    """


class ObjectMapper(object):
    """
    Allows to map objects from one type to another
    """

    def __init__(self):
        self._mappings: Dict[Type[TSource],
                             Dict[Type[TSource], Callable[[TSource], TTarget]]] = {}

    def add(self, source_cls: Type[TSource], target_cls: Type[TTarget], func: Callable[[TSource], TTarget]) -> None:
        """
        Adds a new mapping between two classes
        """
        if self._mappings.get(source_cls) is None:
            self._mappings[source_cls] = {}

        if self._mappings[source_cls].get(target_cls) is not None:
            raise MappingAlreadyExistsException(
                f"Mapping for {source_cls} -> {target_cls} already exists")
        else:
            self._mappings[source_cls][target_cls] = func

    def map(self, target_cls: Type[TTarget],  source: TSource) -> TTarget:
        """
        maps an object to another type
        """
        if self.exist_map(type(source), target_cls) is False:
            raise MappingDoesNotExistException(
                f"Mapping for {type(source)} -> {target_cls} does not exists")

        func = self._mappings[type(source)][target_cls]

        return func(source)

    def exist_map(self, source_cls: Type[TSource], target_cls: Type[TTarget]) -> bool:
        """
        checks if a mapping exists between two classes
        """
        if self._mappings.get(source_cls) is None:
            return False
        elif self._mappings[source_cls].get(target_cls) is None:
            return False
        return True

    def __new__(cls):
        """
        Check if an instance of this class exists to return it, if not create a new one
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(ObjectMapper, cls).__new__(cls)
        return cls.instance


mapper = ObjectMapper()

if __name__ == "__main__":
    class ClassA:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    class ClassB:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    class ClassC:
        def __init__(self, name: str, age: int):
            self.name = name
            self.age = age

    mapper.add(ClassA, ClassB, lambda a: ClassB(
        name=a.name + " extra b", age=a.age if a.age else 100))

    a = ClassA(name="delfin", age=None)

    b = mapper.map(ClassB, a)

    print("a class ", a.name, a.age)
    print("b class ", b.name, b.age)
    print("c class can be mapped? ", mapper.exist_map(ClassA, ClassC))
