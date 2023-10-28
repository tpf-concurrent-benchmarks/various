from typing import Iterator, TypeVar, Generic

T = TypeVar("T")


class CircularIterator(Generic[T]):
    def __init__(self, iterator: Iterator[T], size: int):
        self.iterator = iterator
        self.size = size
        self.position = 0
        self.values = []

    def __repr__(self):
        values = [next(self) for _ in range(self.size)]
        return "[" + ", ".join([str(value) for value in values]) + "]"

    def __next__(self) -> T:
        if self.position == self.size:
            self.position = 0
        if self.position == len(self.values):
            self.values.append(next(self.iterator))
        value = self.values[self.position]
        self.position += 1
        return value
