import pytest
from .priority_scheduler import PriorityScheduler

def snapshot(ps: PriorityScheduler, n: int):
    return [ps.run_next() for _ in range(n)] + [ps.run_next()]  # extra None at end

def test_empty_run_next_returns_none():
    ps = PriorityScheduler()
    assert len(ps) == 0
    assert ps.run_next() is None

def test_basic_ordering_and_len():
    ps = PriorityScheduler()
    ps.add(2, "write tests")
    ps.add(1, "fix bug")
    ps.add(3, "deploy")
    assert len(ps) == 3
    assert snapshot(ps, 3) == ["fix bug", "write tests", "deploy", None]
    assert len(ps) == 0

def test_stability_same_priority_fifo():
    ps = PriorityScheduler()
    ps.add(1, "A")
    ps.add(1, "B")
    ps.add(1, "C")
    assert snapshot(ps, 3) == ["A", "B", "C", None]

def test_reprioritize_behaves_like_new_insertion():
    ps = PriorityScheduler()
    ps.add(2, "write tests")
    ps.add(1, "fix bug")
    ps.add(2, "urgent")
    ps.reprioritize("write tests", 1)  # powinno wejść ZA istniejące priorytety 1
    assert snapshot(ps, 3) == ["fix bug", "write tests", "urgent", None]

def test_cancel_removes_task_silently_and_len_updates():
    ps = PriorityScheduler()
    ps.add(2, "a")
    ps.add(1, "b")
    ps.add(3, "c")
    ps.cancel("b")
    assert len(ps) == 2
    assert snapshot(ps, 2) == ["a", "c", None]
    # cancel nieistniejącego nie rzuca
    ps.cancel("not-there")
    assert len(ps) == 0

def test_add_same_name_treated_as_update():
    ps = PriorityScheduler()
    ps.add(3, "job")
    ps.add(1, "job")  # traktuj jak reprioritize
    ps.add(2, "other")
    assert snapshot(ps, 2) == ["job", "other", None]

def test_multiple_reprioritize_and_cancel():
    ps = PriorityScheduler()
    ps.add(5, "x")
    ps.add(5, "y")
    ps.reprioritize("x", 1)
    ps.reprioritize("y", 1)  # y po x przy tym samym priorytecie
    ps.cancel("x")
    assert snapshot(ps, 1) == ["y", None]

# @pytest.mark.parametrize(
#     "ops,expected",
#     [
#         pytest.param(
#             [("add",2,"a"),("add",1,"b"),("reprioritize","a",1),
#              ("add",1,"c"),("run_next",),("run_next",),("cancel","c"),("run_next",),("run_next",)],
#             ["b","c","a",None],
#             id="functional_scenario"
#         ),
#         pytest.param(
#             [("add",1,"a"),("add",1,"b"),("add",1,"c"),("run_next",),("run_next",),("run_next",),("run_next",)],
#             ["a","b","c",None],
#             id="fifo_stability"
#         ),
#     ],
# )
# def test_functional_runner(ops, expected):
#     """Opcjonalny test: jeśli zrobisz też funkcję process_ops(ops) -> list[str]."""
#     from priority_scheduler import process_ops  # zaimplementuj jeśli chcesz
#     assert process_ops(ops) == expected
