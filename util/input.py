import sys
import inspect
from typing import Generator, Any, List


def _find_file_path() -> str:
    for frame_index in range(3, 13):
        caller_path = inspect.getframeinfo(sys._getframe(frame_index)).filename
        if 'main.py' in caller_path:
            return caller_path

    return ""


def _get_lines(tst: bool = False):
    """Creeërt een generator van de input file. De inhoud is regel voor regel door te lezen. De locatie van de inputfile
    wordt bepaald a.d.h.v. het callende script.
    """
    file_name = 'input - test.txt' if tst else 'input.txt'
    caller_path = _find_file_path()
    input_file = caller_path.replace('main.py', file_name)

    with open(input_file, 'r') as file:
        return [line.strip('\n') for line in file.readlines()]


def get_lines(tst: bool = False) -> Generator[str]:
    """Geeft 1-voor-1 de regels van een input file terug."""
    for line in _get_lines(tst):
        yield line


def get_lines_as_list(tst: bool = False):
    """Geeft 1-voor-1 de regels van een input file terug als een lijst van strings."""
    lines = _get_lines(tst)
    for line in lines:
        return (line if line[-1] != '\n' else line[:-1]).split()


def get_lines_as_nrs(tst: bool = False):
    """Geeft 1-voor-1 de regels van een input file terug als een lijst van integers."""
    lines = _get_lines(tst)
    for line in lines:
        line_list = (line if line[-1] != '\n' else line[:-1]).split()
        return [int(val) for val in line_list]


def get_lines_as_grid(tst: bool = False):
    """Geeft 1-voor-1 de regels van een input file terug als een lijst van losse chars."""
    lines = _get_lines(tst)

    return [[char for char in line] for line in lines]
