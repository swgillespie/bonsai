#!/usr/bin/env python3

import argparse
import tempfile
import difflib
import io
import sys
import os
from subprocess import run, PIPE

from rich import print

def run_file(file: str) -> None:
    with open(file, "r") as f:
        contents = f.readlines()
    with tempfile.TemporaryDirectory() as tempdir:
        out = io.StringIO()
        for line in contents:
            out.write(line)
            if line.startswith("  $"):
                proc = run(line[3:], shell=True, capture_output=True, cwd=tempdir)
                if proc.stdout:
                    for line in proc.stdout.decode("utf-8").splitlines():
                        out.write(f"  {line}" + os.linesep)
                if proc.returncode != 0:
                    out.write(f"  [{proc.returncode}]" + os.linesep)
        print(out.getvalue())


def main(args: argparse.Namespace) -> None:
    run_file(args.file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="run.py", description="Test runner for Bonsai")
    parser.add_argument("-f", "--file", help="Runs the specified test")
    args = parser.parse_args()
    main(args)