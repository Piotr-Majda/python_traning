import pytest
from unique_elements import unique_elements


def generate_list_with_uniques(map_uniques: set[int], length: int):
    return [
        num if num in map_uniques
        else sum(map_uniques)
        for num in range(0, length)
    ]


NUMBERS_CASE = [
    pytest.param([1,2,2,3,4,4,5], [1, 3, 5], id='basic'),
    pytest.param(generate_list_with_uniques({2, 3, 10}, 1000), [2, 3, 10], id='big list'),
    pytest.param(generate_list_with_uniques({5542, 1001, 303}, 10000), [303, 1001, 5542], id='large list'),
    pytest.param([], [], id='Empty'),
    pytest.param([1,1,1], [], id='None unqies'),
    pytest.param([1,2,3,2,1,4], [3,4], id='Not ordered unqies'),
]


@pytest.mark.parametrize('input,expected_output', NUMBERS_CASE)
def test_unique_preserves_order_ut(input, expected_output):
    unique_numbers = unique_elements(input)
    assert unique_numbers == expected_output
