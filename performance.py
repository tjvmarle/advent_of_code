import pstats
from pstats import SortKey

# TODO: Dit kan in de util module om direct in je main.py te kunnen gebruiken


def print_performance_data():
    perf_data = pstats.Stats('performance_data')
    perf_data.strip_dirs()

    perf_data.sort_stats(SortKey.CUMULATIVE)

    perf_data.print_stats(30)


if __name__ == "__main__":
    print_performance_data()
