#!/usr/bin/env python3

import argparse
import tempfile
import difflib
import io
import sys
import os
from subprocess import run, PIPE

from rich import print
from rich.prompt import Prompt

def run_file(file: str, edit: bool) -> None:
    with open(file, "r") as f:
        contents = f.read().splitlines()
    with tempfile.TemporaryDirectory() as tempdir:
        out = io.StringIO()
        for line in contents:
            if line.startswith("  $"):
                out.write(line + os.linesep)
                proc = run(line[3:], shell=True, capture_output=True, cwd=tempdir)
                if proc.stdout:
                    for line in proc.stdout.decode("utf-8").splitlines():
                        line = line.replace(tempdir, "/tmp/tempdir")
                        out.write(f"  {line}" + os.linesep)
                if proc.stderr:
                    for line in proc.stderr.decode("utf-8").splitlines():
                        line = line.replace(tempdir, "/tmp/tempdir")
                        out.write(f"  !{line}" + os.linesep)
                if proc.returncode != 0:
                    out.write(f"  [{proc.returncode}]" + os.linesep)
            elif not line.startswith("  "):
                out.write(line + os.linesep)
        out_lines = out.getvalue().splitlines()
        if contents != out_lines:
            for line in difflib.unified_diff(contents, out.getvalue().splitlines()):
                print(line)
            if args.edit and Prompt.ask("Do you want to update the file? \[y/N] "):
                with open(file, "w") as f:
                    f.truncate(0)
                    f.write(out.getvalue())



def main(args: argparse.Namespace) -> None:
    run_file(args.file, args.edit)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="run.py", description="Test runner for Bonsai")
    parser.add_argument("-f", "--file", help="Runs the specified test")
    parser.add_argument("-e", "--edit", action="store_true", help="Prompt to edit failing tests")
    args = parser.parse_args()
    main(args)