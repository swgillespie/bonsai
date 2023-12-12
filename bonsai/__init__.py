import subprocess
import sys

import click
from rich import print

DEBUG = True

def git_dir() -> str:
    return git("rev-parse", "--git-dir")

def git(*args: str) -> str:
    if DEBUG:
        print(f"[bold blue]> git {' '.join(args)}[/bold blue]")
    return subprocess.check_output(["git"] + list(args), stderr=sys.stderr).decode("utf-8").strip()

def resolve_commit_to_branch(sha: str) -> str:
    branches = git("branch", "--contains", sha).split("\n")
    return branches[1].strip()


@click.group()
def main() -> None:
    """
    Git and GitHub commit stacking utility.
    """
    pass

@main.command()
def up() -> None:
    """
    Move upwards to the next commit in the stack.
    """
    git("checkout", "HEAD@{1}")
    branch = resolve_commit_to_branch("HEAD")
    git("checkout", branch)

@main.command()
def down() -> None:
    """
    Move downwards to the previous commit in the stack.
    """
    git("checkout", "HEAD~")
    branch = resolve_commit_to_branch("HEAD")
    git("checkout", branch)

@main.command()
def commit() -> None:
    print("Creating a new bonsai tree...")