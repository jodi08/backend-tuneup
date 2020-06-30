#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tuneup assignment

Use the timeit and cProfile libraries to find bad code.
"""

__author__ = "Jo Anna Mollman and Pierro and group"

import cProfile
import pstats
import functools
import timeit
from collections import Counter


def profile(func):
    """A cProfile decorator function that can be used to
    measure performance.
    """
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        profile = cProfile.Profile()
        profile.enable()  # start timer
        value = func(*args, **kwargs)  # call original function
        profile.disable()  # end timer

        get_stats_obj = pstats.Stats(profile).strip_dirs().sort_stats("cumulative").print_stats(10)
        return value
        print(f'Best time across 7 repeats of 5 runs per repeat: {value}')
    return wrapper_timer


def read_movies(src):
    """Returns a list of movie titles."""
    print(f'Reading file: {src}')
    with open(src, 'r') as f:
        return f.read().splitlines()


def is_duplicate(title, movies):
    """Returns True if title is within movies list."""
    for movie in movies:
        if movie == title:
            return True
    return False

@profile
def find_duplicate_movies(src):
    """Returns a list of duplicate movies from a src list."""
    movies = read_movies(src)
    c = Counter(movies)
    duplicates = []
    for key, value in c.items():
        if value > 1:
            duplicates.append(key)
    
    return duplicates


def timeit_helper():
    """Part A: Obtain some profiling measurements using timeit."""
    timer_ = timeit.Timer(
        stmt="find_duplicate_movies('movies.txt')",
        setup="from __main__ import find_duplicate_movies"
    )
    runs_per_repeat = 7
    num_repeats = 5
    result = timer_.repeat(
        repeat=num_repeats,
        number=runs_per_repeat)
    best_time = min(result) / runs_per_repeat
    print(f"The best per function time across 7 repeats of 5 runs was {best_time:.2f}")
timeit_helper()


def main():
    """Computes a list of duplicate movie entries."""
    result = find_duplicate_movies('movies.txt')
    print(f'Found {len(result)} duplicate movies:')
    print('\n'.join(result))
    timeit_helper()


if __name__ == '__main__':
    main()
