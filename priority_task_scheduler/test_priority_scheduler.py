import pytest
from .priority_scheduler import TaskScheduler

'''
scheduler = TaskScheduler()
scheduler.add_task("fix bug", 2)
scheduler.add_task("write tests", 1)
scheduler.add_task("refactor", 1)
scheduler.pop_task()  # "write tests"
scheduler.pop_task()  # "refactor"
scheduler.pop_task()  # "fix bug"
"""
'''


@pytest.mark.parametrize(
    "tasks, expected",
    [
        (
            [("fix bug", 2), ("write tests", 1), ("refactor", 1)],
            ["write tests", "refactor", "fix bug", None],
        ),
        (
            [("A", -5), ("B", 0), ("C", -5)],
            ["A", "C", "B", None],
        ),
        (
            [],  # pusta kolejka
            [None],
        ),
    ],
    ids=["priorytety+FIFO", "ujemne_priorytety", "pusta"]
)
def test_scheduler(tasks, expected):
    s = TaskScheduler()
    for name, prio in tasks:
        s.add_task(name, prio)
    out = [s.pop_task() for _ in expected]
    assert out == expected

def test_peek_and_len():
    s = TaskScheduler()
    assert s.peek() is None and len(s) == 0
    s.add_task("X", 10)
    assert s.peek() == "X" and len(s) == 1
