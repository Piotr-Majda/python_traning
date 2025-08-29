import pytest
from .merge_k_sorted import merge_k_sorted, merge_k_sorted_manual, merge_k_sorted_manual_not_optimal


TEST_CASES = [
    pytest.param([[1,4,5],[1,3,4],[2,6]], [1,1,2,3,4,4,5,6], id='three lists with duplicates'),
    pytest.param([[1,4,5],[],[2,6]],            [1,2,4,5,6], id='with empty list'),
    pytest.param([[],[],[]],                    [],           id='all empty'),
    pytest.param([[ -5, -1, 0 ], [ -3, 2 ]],    [ -5, -3, -1, 0, 2 ], id='negatives'),
]

@pytest.mark.parametrize('input_lists, expected', TEST_CASES)
def test_merge_then_sort_lists(input_lists, expected):
    result = merge_k_sorted(input_lists)
    assert result == expected


@pytest.mark.parametrize('input_lists, expected', TEST_CASES)
def test_merge_then_sort_lists_manual(input_lists, expected):
    result = merge_k_sorted_manual(input_lists)
    assert result == expected


@pytest.mark.parametrize('input_lists, expected', TEST_CASES)
def test_merge_then_sort_lists_manual_v2(input_lists, expected):
    result = merge_k_sorted_manual_not_optimal(input_lists)
    assert result == expected
