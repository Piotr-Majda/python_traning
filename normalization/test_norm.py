import pytest
from normalization import normalize_posix_path

NORM_CASES = [
    pytest.param("", ".", id="empty_as_dot"),
    pytest.param("/", "/", id="root"),
    pytest.param("////", "/", id="many_slashes_to_root"),
    pytest.param("././", ".", id="dots_only"),
    pytest.param("a/b/c", "a/b/c", id="simple_relative"),
    pytest.param("a//b/./c/../", "a/b", id="collapse_and_dotdot_relative"),
    pytest.param("/a//b/./c/../", "/a/b", id="collapse_and_dotdot_absolute"),
    pytest.param("a/b/../../c", "c", id="rel_backtrack_to_c"),
    pytest.param("../a/..//b/.", "../b", id="leading_dotdots_preserved"),
    pytest.param("../../", "../..", id="only_dotdots_relative"),
    pytest.param("/../", "/", id="cannot_go_above_root"),
    pytest.param("/a/../../b/../c//.//", "/c", id="mixed_absolute"),
    pytest.param("a/./.././../b", "../b", id="complex_relative_up"),
]

@pytest.mark.parametrize("raw,expected", NORM_CASES)
def test_normalize_posix_path(raw, expected):
    assert normalize_posix_path(raw) == expected
