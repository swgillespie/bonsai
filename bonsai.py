import subprocess
import os

import click
from rich import print

DEBUG = False

def git_dir() -> str:
    return git("rev-parse", "--git-dir")

def git(*args: str) -> str:
    if DEBUG:
        print(f"[bold blue]> git {' '.join(args)}[/bold blue]")
    return subprocess.check_output(["git"] + list(args), stderr=subprocess.DEVNULL).decode("utf-8").strip()

def track_branch(name: str, sha: str) -> None:
    path = os.path.join(git_dir(), "bonsai", "branches", name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        return
    
    with open(path, "w") as f:
        f.write(sha)

def get_tracked_branches() -> list[str]:
    path = os.path.join(git_dir(), "bonsai", "branches")
    if not os.path.exists(path):
        return []
    return os.listdir(path)
 
def resolve_commit_to_branch(sha: str) -> str:
    return git("name-rev", sha, "--name-only").strip()

def resolve_branch_to_commit(name: str) -> str:
    return git("rev-parse", name).strip()


@click.group()
@click.option("--debug/--no-debug", default=False, help="Enable/disable debug logging")
def main(debug: bool) -> None:
    """
    Git and GitHub commit stacking utility.
    """
    global DEBUG
    DEBUG = debug
    pass

@main.command()
def up() -> None:
    """
    Move upwards to the next commit in the stack.
    """
    candidate_branches = []
    for branch in get_tracked_branches():
        commits = git("rev-list", "--reverse", "--topo-order", "--ancestry-path", f"HEAD..{branch}").splitlines()
        if len(commits) > 0:
            candidate_branches.append((branch, commits[0]))
    if not len(candidate_branches):
        print("Unable to find a parent commit to move to - is your current stack tracked?")
    elif len(candidate_branches) == 1:
        _, commit = candidate_branches[0]
        git("checkout", resolve_commit_to_branch(commit))
    else:
        print(candidate_branches)

@main.command()
def down() -> None:
    """
    Move downwards to the previous commit in the stack.
    """
    git("checkout", "HEAD~")
    branch = resolve_commit_to_branch("HEAD")
    git("checkout", branch)

@main.command()
def track() -> None:
    """
    Track the current branch as the tip of a stack.
    """
    branch = resolve_commit_to_branch("HEAD")
    sha = resolve_branch_to_commit(branch)
    path = os.path.join(git_dir(), "bonsai", "branches", branch)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if os.path.exists(path):
        print(f"Branch [bold green]{branch}[/bold green] is already tracked")
        return
    with open(path, "w") as f:
        f.write(sha)
    print(f"Now tracking branch [bold green]{branch}[/bold green]")

@main.command()
def commit() -> None:
    print("Creating a new bonsai tree...")

if __name__ == "__main__":
    main()