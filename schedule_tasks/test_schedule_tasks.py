import pytest
from .schedule_tasks import schedule_tasks


TEST_CASES = [
    pytest.param([(2, "write tests"), (1, "fix bug"), (3, "deploy")], ["fix bug", "write tests", "deploy"]),
    pytest.param([(5, "low"), (1, "high"), (1, "urgent"), (3, "mid")], ["high", "urgent", "mid", 'low']),
]


@pytest.mark.parametrize("tasks,excepted_output", TEST_CASES)
def test_schedule_tasks_ut(tasks, excepted_output):
    result = schedule_tasks(tasks)
    assert result == excepted_output
