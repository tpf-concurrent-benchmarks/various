import math
from typing import Iterator


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
            i = self.__round_number(i + self._step, precision)


    @staticmethod
    def __round_number(x: int | float, precision: int | None) -> int | float:
        if precision is None:
            return x
        return round(x, precision)

    def __split_evenly(self, amount_of_sub_intervals: int, precision: int = None) -> Iterator["Interval"]:
        assert self.size % amount_of_sub_intervals == 0

        for pos in range(amount_of_sub_intervals):
            sub_start = self.__round_number(self._start + pos * self._size // amount_of_sub_intervals * self._step,
                                            precision)
            sub_end = self.__round_number(self._start + (pos + 1) * self._size // amount_of_sub_intervals * self._step,
                                          precision)
            yield Interval(sub_start, sub_end, self._step)
        return

    def split(self, amount_of_sub_intervals: int, precision: int = None) -> Iterator["Interval"]:
        if self.size % amount_of_sub_intervals == 0:
            yield from self.__split_evenly(amount_of_sub_intervals, precision)
            return

        max_elems_per_interval = math.ceil(self._size / amount_of_sub_intervals)
        amount_of_sub_intervals_of_full_size = (self._size - amount_of_sub_intervals) // (max_elems_per_interval - 1)

        sub_end = None
        for pos in range(amount_of_sub_intervals_of_full_size):
            sub_start = self.__round_number(self._start + pos * max_elems_per_interval * self._step, precision)
            sub_end = self.__round_number(min(self._end, sub_start + max_elems_per_interval * self._step), precision)
            yield Interval(sub_start, sub_end, self._step)

        remaining_interval = Interval(sub_end, self._end, self._step)
        remaining_amount_of_sub_intervals = amount_of_sub_intervals - amount_of_sub_intervals_of_full_size
        yield from remaining_interval.split(remaining_amount_of_sub_intervals, precision)
