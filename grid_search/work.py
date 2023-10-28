import math
from functools import reduce
from typing import List, Iterator

from cartesian_product_calculator import CartesianProductCalculator
from circular_iterator import CircularIterator
from interval import Interval


class Work:
    def __init__(self, intervals: List[Interval]):
        self._intervals = intervals
        self._size = self.__calc_size()
        self._dim = len(intervals)

    def __repr__(self):
        return f"{self._intervals}"

    def __getitem__(self, item):
        return self._intervals[item]

    def __iter__(self):
        return iter(self._intervals)

    def __calc_size(self) -> int:
        total = 1
        for interval in self._intervals:
            total *= interval.size
        return total

    @property
    def size(self) -> int:
        return self._size

    def unfold(self, precision: int = None) -> Iterator[List[int | float]]:
        yield from CartesianProductCalculator.calculate([list(interval.unfold(precision)) for interval in self._intervals])

    @staticmethod
    def __calc_partitions_amount(partitions_per_interval: List[int]) -> int:
        return reduce(lambda a, b: a * b, partitions_per_interval)

    def __calc_amount_of_missing_partitions(self, min_batches: int, partitions_per_interval: List[int]) -> int:
        return math.ceil(min_batches / self.__calc_partitions_amount(partitions_per_interval))

    def __calc_partitions_per_interval(self, min_batches: int) -> List[int]:
        curr_partitions_per_interval = [1] * self._dim

        for interval_pos in range(self._dim):
            missing_partitions = self.__calc_amount_of_missing_partitions(min_batches, curr_partitions_per_interval)

            elements = self[interval_pos].size
            if elements > missing_partitions:
                curr_partitions_per_interval[interval_pos] *= missing_partitions
                break
            else:
                curr_partitions_per_interval[interval_pos] *= elements

        return curr_partitions_per_interval

    def split(self, max_chunk_size: int, precision: int = None) -> Iterator["Work"]:
        min_batches = self.size // max_chunk_size + 1
        partitions_per_interval = self.__calc_partitions_per_interval(min_batches)

        lists_of_intervals = []

        for interval_pos in range(self._dim):
            iterator = self[interval_pos].split(partitions_per_interval[interval_pos],
                                                precision)
            iterator = CircularIterator(iterator, partitions_per_interval[interval_pos])
            lists_of_intervals.append(iterator)

        yield from WorkPlan(lists_of_intervals, partitions_per_interval)


class WorkPlan:
    def __init__(self, intervals: List[CircularIterator], intervals_per_iterator: List[int]):
        self._intervals = intervals
        self._intervals_per_iterator = intervals_per_iterator

    def calc_cartesian_product(self) -> Iterator["Work"]:
        positions = [0 for _ in self._intervals]
        prev_positions = [0 for _ in self._intervals]
        current_values = [next(iterator) for iterator in self._intervals]

        for value in self._intervals:
            if not value:
                return

        while True:
            yield Work([current_value for current_value in current_values])

            for i in range(len(self._intervals)):
                positions[i] += 1
                if positions[i] < self._intervals_per_iterator[i]:
                    break
                positions[i] = 0
                if i == len(self._intervals) - 1:
                    return

            for i in range(len(self._intervals)):
                if positions[i] != prev_positions[i]:
                    current_values[i] = next(self._intervals[i])
                    prev_positions[i] = positions[i]
                else:
                    break

    def __iter__(self) -> Iterator["Work"]:
        yield from self.calc_cartesian_product()

    def unfold(self, precision: int = None) -> List[List[int]]:
        result = []
        for chunk in self:
            result.extend(chunk.unfold(precision))
        return result
