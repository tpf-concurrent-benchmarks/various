import math
from functools import reduce

from typing import Tuple, List, NewType, Iterator

Interval = NewType("Interval", Tuple[float, float, float])
Work = NewType("Work", List[Interval])
WorkChunk = NewType("WorkChunk", List[Interval])
WorkPlan = NewType("WorkPlan", Iterator[WorkChunk])



def calc_interval_size(interval: Interval) -> int:
    start, end, step = interval
    return math.ceil((end - start) / step)


def my_range(start, end, step):
    while start < end:
        yield start
        start += step


def split_interval_into_sub_intervals(interval: Interval, n: int, precision: int = None) -> List[Interval]:
    def round_number(x):
        if precision is None:
            return x
        return round(x, precision)

    start, end, step = interval
    interval_size = calc_interval_size(interval)
    if interval_size % n == 0:
        for i in range(n):
            sub_start = round_number(start + i * interval_size // n * step)
            sub_end = round_number(start + (i + 1) * interval_size // n * step)
            yield Interval((sub_start, sub_end, step))
        return

    # Elements of each interval for the first part
    # For the second part, we will split recursively the remaining elements
    k = math.ceil(interval_size / n)
    m = math.floor((interval_size - n) / (k - 1))

    for i in range(m):
        sub_start = round_number(start + i * k * step)
        sub_end = round_number(min(end, sub_start + k * step))
        yield Interval((sub_start, sub_end, step))

    remaining_interval = Interval((sub_end, end, step))
    yield from split_interval_into_sub_intervals(remaining_interval, n - m)


def calc_cartesian_product(lists_of_intervals: List[List[Interval]]) -> WorkPlan:
    positions = [0 for _ in lists_of_intervals]
    max_positions = [len(intervals) for intervals in lists_of_intervals]

    for intervals in lists_of_intervals:
        if not intervals:
            return

    while True:
        yield [lists_of_intervals[i][positions[i]] for i in range(len(lists_of_intervals))]

        for i in range(len(lists_of_intervals) - 1, -1, -1):
            positions[i] += 1
            if positions[i] < max_positions[i]:
                break
            positions[i] = 0
            if i == 0:
                return


def calc_work_size(work: Work) -> int:
    total = 1
    for interval in work:
        total *= calc_interval_size(interval)
    return total


def calc_work_chunk_weight(chunk: WorkChunk | List[Interval]) -> int:
    total = 1
    for start, end, step in chunk:
        total *= math.ceil((end - start) / step)
    return total


def calc_work_weight(work: Work) -> int:
    total = 0
    for interval in work:
        total += calc_work_chunk_weight(interval)
    return total


def calc_partitions_amount(partitions_per_interval: List[int]) -> int:
    return reduce(lambda a, b: a * b, partitions_per_interval)


def calc_amount_of_missing_partitions(min_batches: int, partitions_per_interval: List[int]) -> int:
    return math.ceil(min_batches / calc_partitions_amount(partitions_per_interval))


def calc_partitions_per_interval(work: Work, min_batches: int) -> List[int]:
    dim = len(work)
    curr_partitions_per_interval = [1] * dim

    for interval_pos in range(dim):
        missing_partitions = calc_amount_of_missing_partitions(min_batches, curr_partitions_per_interval)

        elements = calc_interval_size(work[interval_pos])
        if elements > missing_partitions:
            curr_partitions_per_interval[interval_pos] *= missing_partitions
            break
        else:
            curr_partitions_per_interval[interval_pos] *= elements

    return curr_partitions_per_interval


def split_work_into_chunks(work: Work, max_chunk_size: int, precision: int = None) -> WorkPlan:
    total_elements = calc_work_size(work)
    min_batches = total_elements // max_chunk_size + 1
    partitions_per_interval = calc_partitions_per_interval(work, min_batches)

    lists_of_intervals = []
    for interval_pos in range(len(work)):
        lists_of_intervals.append(list(
            split_interval_into_sub_intervals(work[interval_pos], partitions_per_interval[interval_pos], precision)))

    yield from calc_cartesian_product(lists_of_intervals)


def unfold_work(work: Work) -> List[List[int]]:
    return list(calc_cartesian_product([[i for i in my_range(*interval)] for interval in work]))

def unfold_chunk(chunk: WorkChunk) -> List[List[int]]:
    return list(calc_cartesian_product([[i for i in my_range(*interval)] for interval in chunk]))


def unfold_work_plan(work_plan: WorkPlan) -> List[List[int]]:
    result = []
    for chunk in work_plan:
        result.extend(unfold_chunk(chunk))
    return result


def assert_work_is_splitted_correctly(work: Work, max_chunk_size: int):
    print("Work:", work)
    unfolded_work = unfold_work(work)
    unfolded_work = [[round(x, 2) for x in work_unit] for work_unit in unfolded_work]
    print("Unfolded work:", unfolded_work)

    work_plan = split_work_into_chunks(work, max_chunk_size, 2)
    unfolded_work_plan = unfold_work_plan(work_plan)
    unfolded_work_plan = [[round(x, 2) for x in work_unit] for work_unit in unfolded_work_plan]
    print("Unfolded work plan:", unfolded_work_plan)

    for work_unit in unfolded_work:
        try:
            unfolded_work_plan.remove(work_unit)
        except ValueError:
            raise AssertionError(f"Work unit {work_unit} is not in the work plan {unfolded_work_plan}")

    if unfolded_work_plan:
        raise AssertionError(f"Work plan has extra work units not found in the original work: {unfolded_work_plan}")
    print("Work is splitted correctly")


def run_tests():
    assert_work_is_splitted_correctly(Work([Interval((0, 1, 1))]), 1)
    assert_work_is_splitted_correctly(Work([Interval((0, 2, 1))]), 1)
    assert_work_is_splitted_correctly(Work([Interval((0, 2, 1))]), 2)
    assert_work_is_splitted_correctly(Work([Interval((0, 10, 3))]), 1)
    assert_work_is_splitted_correctly(Work([Interval((0, 10, 3))]), 2)
    assert_work_is_splitted_correctly(Work([Interval((0, 10, 4.3))]), 3)
    assert_work_is_splitted_correctly(Work([Interval((0, 3, 1)),
                                            Interval((0, 3, 1))]), 1)
    assert_work_is_splitted_correctly(Work([Interval((0, 3, 1)),
                                            Interval((0, 3, 1))]), 2)
    assert_work_is_splitted_correctly(Work([Interval((0, 10, 1)),
                                            Interval((0, 10, 1)),
                                            Interval((0, 10, 1))]), 13)
    assert_work_is_splitted_correctly(
        Work([Interval((0, 12.3, 8.4)),
              Interval((5.3, 8.99, 1.2)),
              Interval((3, 3.3, 0.1))]), 5)
    assert_work_is_splitted_correctly(
        Work([Interval((0, 12.3, 8.4)),
              Interval((5.3, 8.99, 1.2)),
              Interval((3, 3.3, 0.1)),
              Interval((0, 12.3, 8.4))]), 5)


def main():
    run_tests()


main()
