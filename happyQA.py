import argparse
from pathlib import Path
import re

import typing as t


def read_releases(path: Path) -> t.List[t.Tuple[int, int]]:
    with open(path) as f:
        data = f.read().splitlines()
    result = []
    for n, line in enumerate(data):
        if not re.match(r"^\d+ \d+$", line):
            raise ValueError(f"Line {n}: Each line should contain two integers")
        values = line.split(" ")
        release_day, length = map(int, values)
        release_day = int(release_day)
        length = int(length)
        if release_day > 10 or release_day < 1:
            raise ValueError(
                f"Line {n}: The day of a sprint should be in the range 1..10. Current value is {release_day}"
            )
        if length > 10 or length < 1:
            raise ValueError(
                f"Line {n}: The release length should be in the range 1..10. Current value is {length}"
            )
        result.append((release_day, length))

    return result


def write_result(path: Path, result: t.List[t.Tuple[int, int]]) -> None:
    with open(path, "w+") as f:
        f.write("\n".join(result))


def calculate(releases: t.List[t.Tuple[int, int]]) -> t.List[t.Tuple[int, int]]:
    releases = sorted(
        [
            (release_day + length - 1, release_day, length)
            for release_day, length in releases
            if release_day + length <= 11
        ]
    )
    calculated_result = [None] * 10
    last_release_end = -1
    for end_day, start_day, length in releases:
        current_start_day = max(last_release_end + 1, start_day)

        if current_start_day + length - 1 > 10:
            continue
        calculated_result[current_start_day - 1] = length
        last_release_end = current_start_day + length - 1

    return [(n + 1, n + value) for n, value in enumerate(calculated_result) if value]


def main(input_path: Path, output_path: Path) -> None:
    releases = read_releases(input_path)
    solution = calculate(releases)
    result = [str(len(solution))] + ["{} {}".format(*line) for line in solution]
    write_result(output_path, result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Help Bob")
    parser.add_argument(
        "--input", help="Path to the input file", default="releases.txt"
    )
    parser.add_argument(
        "--output", help="Path to the output file", default="solution.txt"
    )
    args = parser.parse_args()

    main(Path(args.input), Path(args.output))
