#!/usr/bin/env python3

from typing import Optional, Tuple
import re
import pathlib
import sys
import subprocess

def main():
    max_options = 32
    regex = sys.argv[1]
    process = subprocess.run(
        ["locate", "-i", "-r", regex],
        capture_output=True
    )
    options = process.stdout.decode().strip().split("\n")
    n_options = len(options)

    home_dir = str(pathlib.Path.home())
    for i, option in enumerate(options[:max_options]):
        display_name = re.sub("^" + home_dir, "~", option)
        print(i, display_name)
    if n_options > max_options:
        print(f"({n_options - max_options} more not shown.)")

    choice_str, choice_int = get_input(n_options)
    if choice_int is not None:
        command = ["xdg-open"] if len(sys.argv) == 2 else sys.argv[2:]
        subprocess.run(command + [options[choice_int]])
    else:
        print(f"Invalid input \"{choice_str}\" – aborting.")


def get_input(n_options: int) -> Tuple[str, Optional[int]]:
    choice_str = input()
    try:
        choice_int = int(choice_str)
        if not 0 <= choice_int < n_options:
            choice_int = None
    except ValueError:
        choice_int = None
    return choice_str, choice_int
    

if __name__ == "__main__":
    main()
