import math
from functools import reduce

from typing import List, Iterator, TypeVar

T = TypeVar("T")

def calc_cartesian_product(lists_of_values: List[List[T]]) -> Iterator[List[T]]:
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

class Interval:
    def __init__(self, start, end, step):
        self._start = start
        self._end = end
        self._step = step
        self._size = math.ceil((end - start) / step)

    def __repr__(self):
        return f"[{self._start}, {self._end}, {self._step}]"

    @property
    def size(self) -> int:
        return self._size

    def unfold(self, precision: int = None) -> Iterator[int | float]:
        i = self._start
        while i < self._end:
            yield self.__round_number(i, precision)
            i += self._step

    @staticmethod
    def __round_number(x: int | float, precision: int | None) -> int | float:
        if precision is None:
            return x
        return round(x, precision)

    def __split_evenly(self, amount_of_sub_intervals: int, precision: int = None) -> Iterator["Interval"]:
        assert self.size % amount_of_sub_intervals == 0

        for pos in range(amount_of_sub_intervals):
            sub_start = self.__round_number(self._start + pos * self._size // amount_of_sub_intervals * self._step, precision)
            sub_end = self.__round_number(self._start + (pos + 1) * self._size // amount_of_sub_intervals * self._step, precision)
            yield Interval(sub_start, sub_end, self._step)
        return

    def split(self, amount_of_sub_intervals: int, precision: int = None) -> Iterator["Interval"]:
        if self.size % amount_of_sub_intervals == 0:
            yield from self.__split_evenly(amount_of_sub_intervals, precision)
            return

        max_elems_per_interval = math.ceil(self._size / amount_of_sub_intervals)
        amount_of_sub_intervals_of_full_size = math.floor((self._size - amount_of_sub_intervals) / (max_elems_per_interval - 1))

        sub_end = None
        for pos in range(amount_of_sub_intervals_of_full_size):
            sub_start = self.__round_number(self._start + pos * max_elems_per_interval * self._step, precision)
            sub_end = self.__round_number(min(self._end, sub_start + max_elems_per_interval * self._step), precision)
            yield Interval(sub_start, sub_end, self._step)

        remaining_interval = Interval(sub_end, self._end, self._step)
        remaining_amount_of_sub_intervals = amount_of_sub_intervals - amount_of_sub_intervals_of_full_size
        yield from remaining_interval.split(remaining_amount_of_sub_intervals, precision)


class WorkChunk:
    def __init__(self, intervals: List[Interval]):
        self._intervals = intervals

    def unfold(self, precision: int = None) -> List[List[int | float]]:
        return list(calc_cartesian_product([list(interval.unfold(precision)) for interval in self._intervals]))

class WorkPlan:
    def __init__(self, intervals: List[List[Interval]]):
        self._intervals = intervals

    def calc_cartesian_product(self) -> Iterator[WorkChunk]:
        positions = [0 for _ in self._intervals]
        max_positions = [len(intervals) for intervals in self._intervals]

        for intervals in self._intervals:
            if not intervals:
                return

        while True:
            yield WorkChunk([self._intervals[i][positions[i]] for i in range(len(self._intervals))])

            for i in range(len(self._intervals) - 1, -1, -1):
                positions[i] += 1
                if positions[i] < max_positions[i]:
                    break
                positions[i] = 0
                if i == 0:
                    return

    def __iter__(self):
        return self.calc_cartesian_product()

    def unfold(self, precision: int = None) -> List[List[int]]:
        result = []
        for chunk in self:
            result.extend(chunk.unfold(precision))
        return result



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

    def unfold(self, precision: int = None) -> List[List[int | float]]:
        return list(calc_cartesian_product([list(interval.unfold(precision)) for interval in self._intervals]))

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

    def split(self, max_chunk_size: int, precision: int = None) -> WorkPlan:
        min_batches = self.size // max_chunk_size + 1
        partitions_per_interval = self.__calc_partitions_per_interval(min_batches)

        lists_of_intervals = []
        for interval_pos in range(self._dim):
            lists_of_intervals.append(list(
                self[interval_pos].split(partitions_per_interval[interval_pos],
                                                  precision)))

        return WorkPlan(lists_of_intervals)



def assert_work_is_splitted_correctly(work: Work, max_chunk_size: int):
    unfolded_work = work.unfold(precision=2)
    work_plan = work.split(max_chunk_size, precision=2)
    unfolded_work_plan = work_plan.unfold(precision=2)
    unfolded_work_plan = [[round(x, 2) for x in work_unit] for work_unit in unfolded_work_plan]

    for work_unit in unfolded_work:
        try:
            unfolded_work_plan.remove(work_unit)
        except ValueError:
            raise AssertionError(f"Work unit {work_unit} is not in the work plan {unfolded_work_plan}")

    if unfolded_work_plan:
        print(f"WARNING: Work plan has extra work units not found in the original work: {unfolded_work_plan} (It could be a rounding error)")


def run_tests():
    assert_work_is_splitted_correctly(Work([Interval(0, 1, 1)]), 1)

    assert_work_is_splitted_correctly(Work([Interval(0, 2, 1)]), 1)

    assert_work_is_splitted_correctly(Work([Interval(0, 2, 1)]), 2)
    assert_work_is_splitted_correctly(Work([Interval(0, 10, 3)]), 1)
    assert_work_is_splitted_correctly(Work([Interval(0, 10, 3)]), 2)

    assert_work_is_splitted_correctly(Work([Interval(0, 10, 4.3)]), 3)
    assert_work_is_splitted_correctly(Work([Interval(0, 3, 1),
                                            Interval(0, 3, 1)]), 1)
    assert_work_is_splitted_correctly(Work([Interval(0, 3, 1),
                                            Interval(0, 3, 1)]), 2)
    assert_work_is_splitted_correctly(Work([Interval(0, 10, 1),
                                            Interval(0, 10, 1),
                                            Interval(0, 10, 1)]), 13)
    assert_work_is_splitted_correctly(
        Work([Interval(0, 12.3, 8.4),
              Interval(5.3, 8.99, 1.2),
              Interval(3, 3.3, 0.1)]), 5)
    assert_work_is_splitted_correctly(
        Work([Interval(0, 12.3, 8.4),
              Interval(5.3, 8.99, 1.2),
              Interval(3, 3.3, 0.1),
              Interval(0, 12.3, 8.4)]), 5)



def main():
    run_tests()


main()
