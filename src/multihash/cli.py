"""
A minimal CLI for some multihash functionality.

Avoids external dependencies, as multihash is primarily a library.
"""

import argparse
from json import dumps

from multihash import MultiHash


def build_parser():
    """Build the parser for the CLI arguments."""
    parser = argparse.ArgumentParser(description="Compute multiple hashes.")
    parser.add_argument(
        "-c",
        "--chunksize",
        default=128000000,  # 128MB
        type=int,
        help="How much (maximum) of the file to read into RAM at once.",
    )
    parser.add_argument(
        "-a",
        "--algos",
        action="append",
        help="The algorithm to use to hash the target(s). Repeatable.",
    )
    parser.add_argument("filepaths", nargs="+", help="Filepaths to hash.")
    return parser


def compute(filepaths, algos, chunksize):
    """Given the parameters computed the JSON output."""
    return {
        filepath: MultiHash.from_filepath(
            filepath, hashers=algos, chunksize=chunksize
        ).hexdigest()
        for filepath in filepaths
    }


def print_results(results):
    """Print the results."""
    print(dumps(results, indent=2))


def cli():
    """Run a simple CLI interface for multihash to hash files."""
    parser = build_parser()
    args = parser.parse_args()
    result = compute(args.filepaths, args.algos, args.chunksize)
    print_results(result)
