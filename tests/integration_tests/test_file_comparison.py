from pathlib import Path
import tempfile

import pytest

from antiquated.internal.comparison import verify_file_matches_expected_file, IteratorPatterns


def test_file_comparison_passes_with_matching_values():
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_directory_path = Path(temporary_directory)
        path0 = temporary_directory_path.joinpath('file0.txt')
        path1 = temporary_directory_path.joinpath('file1.txt')
        path0.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        path1.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        verify_file_matches_expected_file(path0, path1)

def test_file_comparison_fails_with_unmatched_string_values():
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_directory_path = Path(temporary_directory)
        path0 = temporary_directory_path.joinpath('file0.txt')
        path1 = temporary_directory_path.joinpath('file1.txt')
        path0.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        path1.write_text("""
        hello 1 1.0
        yellow 1 1.0
        """)
        with pytest.raises(AssertionError):
            verify_file_matches_expected_file(path0, path1)

def test_file_comparison_fails_with_unmatched_integer_values():
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_directory_path = Path(temporary_directory)
        path0 = temporary_directory_path.joinpath('file0.txt')
        path1 = temporary_directory_path.joinpath('file1.txt')
        path0.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        path1.write_text("""
        hello 1 1.0
        hello 2 1.0
        """)
        with pytest.raises(AssertionError):
            verify_file_matches_expected_file(path0, path1)

def test_file_comparison_fails_with_unmatched_float_values():
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_directory_path = Path(temporary_directory)
        path0 = temporary_directory_path.joinpath('file0.txt')
        path1 = temporary_directory_path.joinpath('file1.txt')
        path0.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        path1.write_text("""
        hello 1 1.0
        hello 1 2.0
        """)
        with pytest.raises(AssertionError):
            verify_file_matches_expected_file(path0, path1)

def test_file_comparison_with_float_value_tolerances():
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_directory_path = Path(temporary_directory)
        path0 = temporary_directory_path.joinpath('file0.txt')
        path1 = temporary_directory_path.joinpath('file1.txt')
        path0.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        path1.write_text("""
        hello 1 1.0
        hello 1 1.001
        """)
        verify_file_matches_expected_file(path0, path1, number_relative_tolerance=0.1)
        with pytest.raises(AssertionError):
            verify_file_matches_expected_file(path0, path1, number_relative_tolerance=0.00001)

def test_file_comparison_fails_with_significant_newlines():
    with tempfile.TemporaryDirectory() as temporary_directory:
        temporary_directory_path = Path(temporary_directory)
        path0 = temporary_directory_path.joinpath('file0.txt')
        path1 = temporary_directory_path.joinpath('file1.txt')
        path0.write_text("""
        hello 1 1.0
        hello 1 1.0
        """)
        path1.write_text("""
        hello 1 1.0 hello 1 1.0
        """)
        verify_file_matches_expected_file(path0, path1, iterator_pattern=IteratorPatterns.WHITE_SPACE_VS_OTHER)
        with pytest.raises(AssertionError):
            verify_file_matches_expected_file(
                path0, path1, iterator_pattern=IteratorPatterns.WHITE_SPACE_VS_OTHER_WITH_SIGNIFICANT_NEWLINES)
