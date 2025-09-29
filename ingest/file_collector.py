import os
from . import config
from .logger import logger
from typing import List


def collect_target_files(base_path: str) -> List[str]:
    """
    Recursively collects all relevant files from a base path, intelligently
    skipping specified directories and file extensions.

    Args:
        base_path (str): The root directory to start searching from.

    Returns:
        List[str]: A list of absolute file paths for all matched files.
    """
    matched_files = []
    # Use os.walk to traverse the directory tree from the base path.
    for root, dirs, files in os.walk(base_path):
        # Modify dirs in-place to prevent os.walk from entering ignored directories.
        dirs[:] = [d for d in dirs if d not in config.IGNORE_DIRS]

        # Iterate through each file found in the current directory.
        for filename in files:
            # Split the filename to get its extension.
            _, file_ext = os.path.splitext(filename)

            # Add the file to the list if its extension is not in the ignore list.
            if file_ext not in config.IGNORE_EXTS:
                file_path = os.path.join(root, filename)
                matched_files.append(file_path)

    return matched_files


# This block allows the script to be run directly for testing purposes.
if __name__ == "__main__":
    # Load configuration for the target repository and file extensions.
    target_repo = config.TARGET_REPO_PATH
    extensions = config.FILE_EXTENSIONS

    # Collect all the target files from the specified repository.
    files = collect_target_files(target_repo, extensions)

    # Log the total number of files found and display the first 10.
    logger.info(f"[+] Found {len(files)} files:")
    for f in files[:10]:
        logger.info(f"\u2514\u2500\u2500 {os.path.relpath(f, target_repo)}")
