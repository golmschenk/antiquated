import mmap
import re
from pathlib import Path

import pytest


def verify_file_matches_expected_file(
        file_path: Path,
        expected_file_path: Path,
        number_relative_tolerance: float = 0.01,
        iterator_pattern: str = r'\s+|[^\s]+',
):
    r"""
    TODO: Make documentation.
    TODO: Add test.

    To make newlines significant white space, set the iterator pattern to `r'[^\S\n\r]+|\n|\r|[^\s]+'`.

    :param file_path:
    :param expected_file_path:
    :param number_relative_tolerance:
    :param iterator_pattern:
    :return:
    """
    with expected_file_path.open() as expected_file_handle, file_path.open() as file_handle:
        line_number = 1
        pattern = re.compile(iterator_pattern)
        memory_map = mmap.mmap(file_handle.fileno(), 0)
        expected_memory_map = mmap.mmap(expected_file_handle.fileno(), 0)
        pattern_iterator = pattern.finditer(memory_map)
        expected_pattern_iterator = pattern.finditer(expected_memory_map)
        for (match, expected_match) in zip(pattern_iterator, expected_pattern_iterator):
            string = match.string
            expected_string = expected_match.string
            expected_white_space_match = re.fullmatch(r'\s+', expected_string)
            if expected_white_space_match is not None:
                actual_white_space_match = re.fullmatch(r'\s+', string)
                assert actual_white_space_match is not None, f'''
                    When comparing the expected {expected_file_path} and the actual {file_path}
                    on line {line_number}, expected a segment of white space and found {string}.  
                '''
                if '\n' in expected_string:
                    line_number += 1
                continue
            try:
                number = float(string)
                expected_number = float(expected_string)
                assert number == pytest.approx(expected_number, rel=number_relative_tolerance), f'''
                    When comparing the expected {expected_file_path} and the actual {file_path}
                    on line {line_number}, the number {expected_number} was expected and the actual was {number}
                    which does not match to a relative tolerance of {number_relative_tolerance}.  
                '''
                continue
            except ValueError:
                assert string == expected_string, f'''
                    When comparing the expected {expected_file_path} and the actual {file_path}
                    on line {line_number}, the string {expected_string} was expected and the actual was {string}.  
                '''
                continue
