import os
import glob


def collect_target_files(base_path, extensions):
  matched_files = []
  for ext in extensions:
    pattern = os.path.join(base_path, "**", f"*{ext}")
    matched_files.extend(glob.glob(pattern, recursive=True))
  return matched_files


if __name__ == "__main__":
  target_repo = "../../cookiecutter-django"
  extensions = ['.md', '.py', '.json', '.toml', '.txt', 'yml']

  files = collect_target_files(target_repo, extensions)

  print(f"[+] Found {len(files)} files:")
  for f in files[:10]:
    print("\u2514\u2500\u2500", os.path.relpath(f, target_repo))