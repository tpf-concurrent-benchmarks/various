from typing import TypeVar

from interval import Interval
from work import Work

T = TypeVar("T")


def assert_work_is_split_correctly(work: Work, max_chunk_size: int):
    unfolded_work = list(work.unfold(precision=10))
    unfolded_work_length = len(unfolded_work)
    sub_works = list(work.split(max_chunk_size, precision=10))
    unfolded_sub_works = []
    for sub_work in sub_works:
        unfolded_sub_work = list(sub_work.unfold(precision=10))
        unfolded_sub_works += unfolded_sub_work

    for work_unit in unfolded_work:
        try:
            unfolded_sub_works.remove(work_unit)
        except ValueError:
            raise AssertionError(f"Work unit {work_unit} is not in the list of sub works {unfolded_sub_works}")

    if unfolded_sub_works:
        remaining_work_length = len(unfolded_sub_works)
        remaining_percentage = remaining_work_length / unfolded_work_length * 100
        print(
            f"WARNING: Sub works have extra work units not found in the original work ({remaining_percentage}% of the original work")
    else:
        print("Work is split correctly")


def run_tests():
    assert_work_is_split_correctly(Work([Interval(0, 1, 1)]), 1)
    assert_work_is_split_correctly(Work([Interval(-1, 0, 1)]), 1)
    assert_work_is_split_correctly(Work([Interval(0, 2, 1)]), 1)
    assert_work_is_split_correctly(Work([Interval(0, 2, 1)]), 2)
    assert_work_is_split_correctly(Work([Interval(0, 10, 3)]), 1)
    assert_work_is_split_correctly(Work([Interval(0, 10, 3)]), 2)
    assert_work_is_split_correctly(Work([Interval(-10, 0, 3)]), 1)
    assert_work_is_split_correctly(Work([Interval(-10, 0, 3)]), 2)
    assert_work_is_split_correctly(Work([Interval(0, 10, 4.3)]), 3)

    assert_work_is_split_correctly(Work([Interval(-10, 0, 4.3)]), 3)
    assert_work_is_split_correctly(Work([Interval(0, 4, 1),
                                         Interval(0, 2, 1)]), 7)

    assert_work_is_split_correctly(Work([Interval(0, 3, 1),
                                         Interval(0, 3, 1)]), 2)
    assert_work_is_split_correctly(Work([Interval(0, 10, 1),
                                         Interval(0, 10, 1),
                                         Interval(0, 10, 1)]), 13)


    assert_work_is_split_correctly(
        Work([Interval(0, 12.3, 8.4),
              Interval(5.3, 8.99, 1.2),
              Interval(3, 3.3, 0.1)]), 5)


    assert_work_is_split_correctly(
        Work([Interval(0, 12.3, 8.4),
              Interval(5.3, 8.99, 1.2),
              Interval(3, 3.3, 0.1),
              Interval(0, 12.3, 8.4)]), 5)

    assert_work_is_split_correctly(
        Work([Interval(-6.5, -5, 0.01)]), 5)

    assert_work_is_split_correctly(
        Work([Interval(0, 12, 3),
              Interval(-8, 4, 2),
              Interval(3, 12, 3)]), 5)


def main():
    run_tests()


main()
