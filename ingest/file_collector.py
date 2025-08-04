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

    for ext in extensions:
        pattern = os.path.join(base_path, "**", f"*{ext}")
        matched_files.extend(glob.glob(pattern, recursive=True))

    return matched_files


if __name__ == "__main__":

    target_repo = config.TARGET_REPO_PATH
    extensions = config.FILE_EXTENSIONS

    files = collect_target_files(target_repo, extensions)

    logger.info(f"[+] Found {len(files)} files:")

    for f in files[:10]:
        logger.info(f"\u2514\u2500\u2500 {os.path.relpath(f, target_repo)}")
