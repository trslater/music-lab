"""Musical scale combinatorics tool

Note: `scale` always refers to a 12-bit binary tuple, where elements represent
the 12 notes of the 12-tone equal tempermant scale, e.g., the major scale would
be (1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1).
"""

from collections import Counter
from itertools import compress, count
import sys

NUM_NOTES = 12


def main():
    m = int(sys.argv[1])

    uniques = set()
    
    for seed in range(2**NUM_NOTES):
        scale = tuple(map(int, bin_pad(seed, NUM_NOTES)))

        if not any(mode in uniques for mode in rotations(scale)):
            uniques.add(scale)
    
    m_atonics = set(s for s in uniques if is_n_atonic(s, m))
    simple = set(s for s in m_atonics if contains_only(s, 1, 2, 3))

    ways = set()
    for scale in simple:
        counts = Counter(intervals(scale))
        counts.update({1: 0, 2: 0, 3: 0})
        ways.add(tuple(b for _, b in sorted(counts.items())))
    
    for way in ways:
        print(way)


def bin_pad(decimal, width):
    """Given a `decimal` number, returns a string representation, padded with
    zeroes to the given `width`"""

    return f"{decimal:0>{width}b}"


def rotations(sequence):
    """Given a `sequence` returns a generator that generates all of its
    rotations, rotating left by 1 each iteration."""

    for _ in range(len(sequence)):
        sequence = rotated(sequence)
        yield sequence


def rotated(sequence, n=1):
    """Given a `sequence`, returns a new sequence rotated `n` to the left."""

    return sequence[n:] + sequence[:n]


def n_atonics(scales, n):
    """Given a set of `scales`, returns only those containing `n` notes"""

    return set(s for s in scales if is_n_atonic(s, n))


def is_n_atonic(scale, n) -> bool:
    """Given a `scale`, returns whether it has `n` notes or not."""

    return sum(map(int, scale)) == n


def contains_only(scale, *allowed_intervals):
    """Given a `scale`, returns whether it contains
    *only* `allowed_intervals`"""
    
    return all(i in allowed_intervals for i in intervals(scale))


def positions(scale):
    """Given a `scale`, returns note positions"""

    return tuple(compress(count(1), scale))


def intervals(scale):
    """Given a `scale`, returns the intervals between notes"""

    p = positions(scale)

    return tuple((b - a) % NUM_NOTES for a, b in zip(p, rotated(p)))


if __name__ == "__main__":
    main()
