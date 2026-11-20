import mmap
import re
from enum import StrEnum
from pathlib import Path

import pytest


class IteratorPatterns(StrEnum):
    WHITE_SPACE_VS_OTHER = r'\s+|[^\s]+'
    WHITE_SPACE_VS_OTHER_WITH_SIGNIFICANT_NEWLINES = r'[^\S\n\r]+|\n|\r|[^\s]+'


def verify_file_matches_expected_file(
        actual_file_path: Path,
        expected_file_path: Path,
        number_relative_tolerance: float = 0.001,
        iterator_pattern: str = IteratorPatterns.WHITE_SPACE_VS_OTHER,
) -> None:
    """
    Compares two files contents during a pytest run. Intended to compare an output file of a process with an expected
    output file. Float values are allowed some tolerance (intended to account for small numerical changes due to
    compiler differences and algorithm refactoring). Iterates over elements and compares them.

    :param actual_file_path: The path of the output file.
    :param expected_file_path: The path of the file that is the expected output.
    :param number_relative_tolerance: The relative tolerance of the float values in the file.
    :param iterator_pattern: The pattern to iterate elements over. Defaults to IteratorPatterns.WHITE_SPACE_VS_OTHER.
                             Use IteratorPatterns.WHITE_SPACE_VS_OTHER_WITH_SIGNIFICANT_NEWLINES to make new lines
                             significant.
    """
    with expected_file_path.open() as expected_file_handle, actual_file_path.open() as actual_file_handle:
        line_number = 1
        pattern = re.compile(iterator_pattern.encode('utf-8'))
        actual_memory_map = mmap.mmap(actual_file_handle.fileno(), 0, access=mmap.ACCESS_READ)
        expected_memory_map = mmap.mmap(expected_file_handle.fileno(), 0, access=mmap.ACCESS_READ)
        actual_pattern_iterator = pattern.finditer(actual_memory_map)
        expected_pattern_iterator = pattern.finditer(expected_memory_map)
        for (actual_match, expected_match) in zip(
                actual_pattern_iterator, expected_pattern_iterator):
            actual_string = actual_match.group().decode()
            expected_string = expected_match.group().decode()
            expected_white_space_match = re.fullmatch(r'\s+', expected_string)
            if expected_white_space_match is not None:
                actual_white_space_match = re.fullmatch(r'\s+', actual_string)
                assert actual_white_space_match is not None, f'''
                    When comparing the expected {expected_file_path} and the actual {actual_file_path}
                    on line {line_number}, expected a segment of white space and found {actual_string}.  
                '''
                if '\n' in expected_string:
                    line_number += 1
                continue
            try:
                actual_number = float(actual_string)
                expected_number = float(expected_string)
                assert actual_number == pytest.approx(expected_number, rel=number_relative_tolerance), f'''
                    When comparing the expected {expected_file_path} and the actual {actual_file_path}
                    on line {line_number}, the number {expected_number} was expected and the actual was {actual_number}
                    which does not match to a relative tolerance of {number_relative_tolerance}.  
                '''
                continue
            except ValueError:
                assert actual_string == expected_string, f'''
                    When comparing the expected {expected_file_path} and the actual {actual_file_path}
                    on line {line_number}, the string {expected_string} was expected and the actual was {actual_string}.  
                '''
                continue
