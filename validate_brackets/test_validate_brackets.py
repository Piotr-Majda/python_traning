import pytest
from .validate_brackets import validate_brackets

TEST_CASES = [
    pytest.param("()[]{}", True),
    pytest.param("([{}])", True),
    pytest.param("(]", False),
    pytest.param("([)]", False),
    pytest.param("abc(def)[ghi]{j}", True),
    pytest.param("(((", False),
    pytest.param("", True),
    pytest.param("]", False),
    pytest.param("{[}", False),
]


@pytest.mark.parametrize("brackets,excepted_output", TEST_CASES)
def test_validate_brackets_ut(brackets, excepted_output):
    result = validate_brackets(brackets)
    assert result == excepted_output
