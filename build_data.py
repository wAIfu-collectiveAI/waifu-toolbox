import argparse
import logging
import random

import yaml
import ujson

from toolbox.core import TrainingExampleGenerator, TurnTooLargeError
from toolbox.filters import NAME_TO_FILTER_MAPPING
from toolbox.formats import NAME_TO_FORMAT_MAPPING
from toolbox.tasks import NAME_TO_TASK_MAPPING

LOG = logging.getLogger(__name__)

def main() -> None:
    args = _parse_args_from_argv()
    logging.basicConfig(
        format='[%(asctime)s] [%(levelname)s] %(message)s',
        level=logging.INFO,
    )

    random.seed(args.seed)

    # Generate tasks and filters by loading from config file.
    with open(args.config, "r") as f:
        task_configs = yaml.safe_load(f)

    formatter = NAME_TO_FORMAT_MAPPING[args.format.lower()]()

    # Open JSONL file.
    f = open(args.output_file, "w", encoding="utf-8")

    all_tasks = []
    for task in args.tasks.split(","):
        kwargs = task_configs[task]
        # Add in filters
        kwargs["filters"] = [NAME_TO_FILTER_MAPPING[f]() for f in kwargs["filters"]]
        all_tasks.append(NAME_TO_TASK_MAPPING[task](**kwargs))

    for task in all_tasks:
        for episode in task:
            try:
                for example in TrainingExampleGenerator(
                    episode=episode,
                    target_token_count=args.max_length,
                    formatter=formatter,
                ):
                    # Dump the example dictionary into a JSONL file.
                    f.write(ujson.dumps(example.formatted_episode) + "\n")
            except TurnTooLargeError:
                LOG.info(f"Skipping over episode {episode.identifier} due to a TurnTooLargeError")

    f.close()
    print(f"Dataset compilation complete!")

def _parse_args_from_argv() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--tasks",
        type=str,
        required=True,
        help="The tasks to build data for, comma-separated."
    )

    parser.add_argument(
        "--config",
        type=str,
        required=True,
        help="The path to the task configuration file."
    )

    parser.add_argument(
        "--output-file",
        type=str,
        required=True,
        help="The JSONL file to write the data to."
    )

    parser.add_argument(
        "--format",
        type=str,
        required=True,
        help="The format to represent the data in."
    )

    parser.add_argument(
        "--max-length",
        type=int,
        default=4096,
        help="The number of tokens (exact or approximate depending on settings) to cap conversations to."
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="The number of tokens (exact or approximate depending on settings) to cap conversations to."
    )

    return parser.parse_args()

if __name__ == "__main__":
    main()