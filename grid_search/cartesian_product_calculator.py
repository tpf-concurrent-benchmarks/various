from typing import List, Iterator, TypeVar, Generic

from circular_iterator import CircularIterator

T = TypeVar("T")

class CartesianProductCalculator(Generic[T]):
    @staticmethod
    def calculate_with_iterators(list_of_iterators: List[CircularIterator[T]], size_of_each_iterator: List[int]) -> Iterator[List[T]]:
        positions = [0 for _ in list_of_iterators]
        prev_positions = [0 for _ in list_of_iterators]
        current_values = [next(iterator) for iterator in list_of_iterators]

        max_positions = size_of_each_iterator

        for value in list_of_iterators:
            if not value:
                return

        while True:
            yield current_values

            for i in range(len(list_of_iterators) - 1, -1, -1):
                positions[i] += 1
                if positions[i] < max_positions[i]:
                    break
                positions[i] = 0
                if i == 0:
                    return

            for i in range(len(list_of_iterators) - 1, -1, -1):
                if positions[i] != prev_positions[i]:
                    current_values[i] = next(list_of_iterators[i])
                    prev_positions[i] = positions[i]
                else:
                    break

    @staticmethod
    def calculate(lists_of_values: List[List[T]]) -> Iterator[List[T]]:
        positions = [0 for _ in lists_of_values]
        max_positions = [len(intervals) for intervals in lists_of_values]

        for value in lists_of_values:
            if not value:
                return

        while True:
            yield [lists_of_values[i][positions[i]] for i in range(len(lists_of_values))]

            for i in range(len(lists_of_values) - 1, -1, -1):
                positions[i] += 1
                if positions[i] < max_positions[i]:
                    break
                positions[i] = 0
                if i == 0:
                    return
