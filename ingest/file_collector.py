import os
import glob
from . import config
from .logger import logger
from typing import List


def collect_target_files(base_path: str, extensions: List[str]) -> List[str]:
    """Recursively collects files with specified extensions from a base path.

    Args:
        base_path (str): The root directory to start searching from.
        extensions (List[str]): A list of file extensions to match (e.g., ['.py', '.md']).

    Returns:
        List[str]: A list of absolute file paths for all matched files.
    """
    matched_files = []
    # Iterate through each specified file extension.
    for ext in extensions:
        # Create a recursive search pattern for the current extension.
        pattern = os.path.join(base_path, "**", f"*{ext}")
        # Use glob to find all files matching the pattern and add them to the list.
        matched_files.extend(glob.glob(pattern, recursive=True))

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
