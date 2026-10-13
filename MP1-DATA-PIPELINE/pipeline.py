"""Run the complete configurable data pipeline."""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    process_data,
    save_data,
    setup_logging,
    validate_dataframe,
    validate_input,
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Load, validate, clean, and save data."
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="Input data file path",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        help="Output CSV file path",
    )
    parser.add_argument(
        "--config",
        required=True,
        help="YAML configuration file path",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable detailed logging",
    )

    return parser.parse_args()


def main():
    """Coordinate loading, validation, processing, and saving."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug("Arguments: %s", args)

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError as error:
        logger.error("Loading failed: %s", error)
        sys.exit(1)

    validation = config["validation"]
    rows_before_validation = len(data)

    try:
        validated_data = validate_dataframe(
            data,
            required_columns=validation["required_columns"],
            numeric_columns=validation["numeric_columns"],
        )
    except ValueError as error:
        logger.error("Validation failed: %s", error)
        sys.exit(1)

    logger.info(
        "Validation complete: %s -> %s rows",
        rows_before_validation,
        len(validated_data),
    )

    original_data = validated_data.copy()

    try:
        cleaned_data = process_data(validated_data, config)
    except ValueError as error:
        logger.error("Processing failed: %s", error)
        sys.exit(1)

    report = create_cleaning_report(original_data, cleaned_data)

    logger.info(
        "Processing complete: %s -> %s rows",
        len(original_data),
        len(cleaned_data),
    )

    output_path = save_data(cleaned_data, args.output)
    logger.info("Saved cleaned data to %s", output_path)

    print("\nCleaning report:")
    print(report)


if __name__ == "__main__":
    main()