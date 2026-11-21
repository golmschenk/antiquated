from pathlib import Path

import pytest

from antiquated.internal.comparison import verify_file_lists_match


def test_verify_file_lists_match():
    actual_paths0 = [Path('1.a'), Path('2.a')]
    expected_paths0 = [Path('2.a'), Path('1.a')]

    verify_file_lists_match(actual_paths0, expected_paths0)

    actual_paths1 = [Path('1.a')]
    expected_paths1 = [Path('2.a'), Path('1.a')]

    with pytest.raises(AssertionError):
        verify_file_lists_match(actual_paths1, expected_paths1)

    actual_paths2 = [Path('1.a'), Path('2.a')]
    expected_paths2 = [Path('1.a')]

    with pytest.raises(AssertionError):
        verify_file_lists_match(actual_paths2, expected_paths2)

    actual_paths3 = [Path('2.a')]
    expected_paths3 = [Path('1.a')]

    with pytest.raises(AssertionError):
        verify_file_lists_match(actual_paths3, expected_paths3)