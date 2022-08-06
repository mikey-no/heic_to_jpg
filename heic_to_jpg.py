import argparse
import logging
import pathlib
import sys

import pillow_heif
from PIL import Image

version = "1.0.0"
description = "Convert heif files to jpg files"
re_file_filter = r"*.heif"

log_format = "[%(asctime)s.%(msecs)03d] %(levelname)-8s %(name)-12s %(lineno)d %(funcName)s - %(message)s"
log_date_format = "%Y-%m-%d %H:%M:%S"

# show all messages below in order of seriousness
log_level = logging.DEBUG  # shows all
# log_level = logging.INFO  # shows info and below
# log_level = logging.WARNING
# log_level = logging.ERROR
# log_level = logging.CRITICAL

logging.basicConfig(
    # Define logging level
    level=log_level,
    # Define the date format
    datefmt=log_date_format,
    # Declare the object we created to format the log messages
    format=log_format,
    # Force this log handler to take over the others that may have been declared in other modules
    # see: https://github.com/python/cpython/blob/3.8/Lib/logging/__init__.py#L1912
    force=True,
    # Declare handlers
    handlers=[
        logging.FileHandler("heic_to_jpg.log", encoding="UTF-8"),
        logging.StreamHandler(sys.stdout),
    ],
)

log = logging.getLogger(__name__)


def convert_file(
    source_file: pathlib.Path, destination_file: pathlib
) -> pathlib.Path | None:
    try:
        heif_file = pillow_heif.open_heif(source_file)
    except Exception as e:
        log.error(f"Error reading in the heif file: {source_file} - {e}")
        return None

    try:
        image = Image.frombytes(
            heif_file.mode,
            heif_file.size,
            heif_file.data,
            "raw",
        )
    except Exception as e:
        log.error(f"Error: parsing the input file: {source_file} - {e}")
        return None
    try:
        if destination_file.exists() is False:
            image.save(destination_file, format("jpeg"))
        else:
            log.error(
                f"Destination file of the same name file found. NOT saved this file: {destination_file}"
            )
    except Exception as e:
        log.error(f"Error: saving the file: {destination_file} - {e}")
        return None
    return destination_file


def main():
    args_parser = argparse.ArgumentParser(description=description)
    args_parser.add_argument(
        "-s",
        "--source",
        dest="source",
        type=pathlib.Path,
        help="Searches for *.heic files to try convert to jpg files of the same name, but with an "
        "additional .jpg extension",
    )
    args_parser.add_argument(
        "-d",
        "--destination",
        dest="destination",
        type=pathlib.Path,
        help="if not supplied then source directory is used",
    )
    args_parser.add_argument(
        "-v",
        "--version",
        dest="version",
        help="get version information then exit",
        action="store_true",  # no extra value after the parameter
    )
    # log.debug(args_parser)
    args = args_parser.parse_args()

    if args.version:
        print(f"Version: {version}")
        sys.exit(0)

    log.debug(args)

    if args.source is None:
        log.critical(f"Error: source directory argument missing")
        sys.exit(1)

    source_dir = pathlib.Path(args.source).resolve()
    destination_dir = pathlib.Path(args.destination).resolve()

    if source_dir.exists() is False:
        log.critical(f"source_dir (or file) not found: {source_dir}")
        sys.exit(2)

    if destination_dir.exists() is False:
        log.warning(f"destination_dir not found: {destination_dir}")
    else:
        destination_dir = source_dir
        log.info(
            f"setting the destination dir to be the same as the source: {destination_dir}"
        )

    if destination_dir.is_dir() is False:
        log.critical(f"destination_dir is not a directory or folder: {destination_dir}")
        sys.exit(3)

    log.info(f"source: {source_dir} - {re_file_filter}")
    log.info(f"destination: {destination_dir}")

    source_file_list = source_dir.glob(re_file_filter)

    index = 0
    conversion_error_counter = 0
    for index, source_file in enumerate(source_file_list, start=1):
        # if index > 10:
        #     break
        destination_file = destination_dir / f"{source_file.name}.jpg"
        # log.info(f'Source file: {source_file} - Destination file: {destination_file}')
        result = convert_file(source_file, destination_file)

        if result is not None:
            log.info(f">>> File count: {index} - saved: {result}")
        else:
            conversion_error_counter = conversion_error_counter + 1

    log.info(
        f"Number of errors: {conversion_error_counter} out of {index} file(s) found"
    )


if __name__ == "__main__":
    main()
