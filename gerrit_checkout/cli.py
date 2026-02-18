"""Command-line interface for gerrit-checkout."""

import argparse
import sys


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch and checkout Gerrit changes related to a Topic into your local Git workspace"
    )
    parser.add_argument(
        "topic",
        help="Gerrit topic to fetch changes for"
    )
    parser.add_argument(
        "--gerrit-url",
        default="https://gerrit.example.com",
        help="Gerrit instance URL (default: https://gerrit.example.com)"
    )
    parser.add_argument(
        "--repo",
        help="Git repository path (default: current directory)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    # TODO: Implement the main functionality
    print(f"Fetching changes for topic: {args.topic}")
    print(f"Gerrit URL: {args.gerrit_url}")
    print(f"Verbose: {args.verbose}")

    sys.exit(0)


if __name__ == "__main__":
    main()
