"""Command-line interface for gerrit-checkout."""

import argparse
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import rich.console

console = rich.console.Console()

GERRIT_SERVER = "csp-gerrit-ssh.volvocars.net"


def _load_manifest_project_paths(manifest_file: Path) -> Dict[str, str]:
    """Load project paths from manifest file.
    
    Args:
        manifest_file: Path to manifest/default.xml
        
    Returns:
        Dictionary mapping project names to local paths
    """
    try:
        tree = ElementTree.parse(manifest_file)
    except ElementTree.ParseError as exc:
        console.print(f"[red]Error: Failed to parse manifest: {manifest_file} ({exc})[/red]")
        sys.exit(1)

    project_paths: Dict[str, str] = {}
    for project in tree.findall(".//project"):
        name = project.get("name")
        path = project.get("path")
        if not name or not path:
            continue
        clean_name = name[:-4] if name.endswith(".git") else name
        project_paths[clean_name] = path
    return project_paths


def _query_gerrit_ssh(topic: str, user: str, gerrit_server: str = GERRIT_SERVER) -> List[Tuple[str, str, str, str]]:
    """Query Gerrit using SSH for changes with given topic.
    
    Args:
        topic: Gerrit topic name
        user: SSH username
        gerrit_server: Gerrit server hostname
        
    Returns:
        List of tuples: (project, change_number, ref, subject)
    """
    cmd = [
        "ssh",
        f"{user}@{gerrit_server}",
        "gerrit",
        "query",
        "--current-patch-set",
        "--format=JSON",
        f"topic:{topic}",
        "status:open",
    ]
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]Error: Gerrit SSH query failed ({exc})[/red]")
        sys.exit(1)

    changes: List[Tuple[str, str, str, str]] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            payload = json.loads(line)
        except json.JSONDecodeError:
            continue
        if payload.get("type") == "stats":
            continue
        project = payload.get("project")
        number = payload.get("number")
        subject = payload.get("subject", "")
        current = payload.get("currentPatchSet") or {}
        ref = current.get("ref")
        if project and number and ref:
            changes.append((str(project), str(number), str(ref), str(subject)))
    return changes


def _checkout_change(
    repo_dir: Path, 
    project: str, 
    ref: str, 
    user: str, 
    gerrit_server: str = GERRIT_SERVER
) -> bool:
    """Checkout a Gerrit change into the repository.
    
    Args:
        repo_dir: Path to git repository
        project: Gerrit project name
        ref: Gerrit ref to fetch
        user: SSH username for Gerrit
        gerrit_server: Gerrit server hostname
        
    Returns:
        True if checkout succeeded, False otherwise
    """
    clean_project = project[:-4] if project.endswith(".git") else project
    parts = ref.split("/")
    if len(parts) < 5:
        console.print(f"[yellow]Skipping: Invalid ref format: {ref}[/yellow]")
        return False

    change_num = parts[3]
    patchset_num = parts[4]
    change_suffix = change_num[-2:]
    fetch_ref = f"refs/changes/{change_suffix}/{change_num}/{patchset_num}"
    fetch_url = f"ssh://{user}@{gerrit_server}/{clean_project}.git"
    fetch_cmd = ["git", "fetch", fetch_url, fetch_ref]

    console.print("----------------------------------------")
    console.print(f"Repo: {repo_dir}")
    console.print(f"Executing: {' '.join(fetch_cmd)} && git checkout FETCH_HEAD")

    try:
        subprocess.run(fetch_cmd, cwd=str(repo_dir), check=True, capture_output=True, text=True)
        subprocess.run(["git", "checkout", "FETCH_HEAD"], cwd=str(repo_dir), check=True, capture_output=True, text=True)
        console.print(f"[green]✓ Successfully checked out change #{change_num}[/green]")
        return True
    except subprocess.CalledProcessError as exc:
        console.print(f"[red]✗ FAILED for project: {project}[/red]")
        return False


def checkout(topic: str, cwd: Optional[str] = None, gerrit_server: str = GERRIT_SERVER) -> None:
    """Fetch Gerrit topic and checkout patchsets.

    Args:
        topic: Gerrit topic name/number
        cwd: Working directory (can be repo root or single git repo).
             If not provided, uses current working directory.
        gerrit_server: Gerrit server hostname
    """
    work_dir = Path(cwd).expanduser().resolve() if cwd else Path.cwd().resolve()
    
    user = os.environ.get("USER", "")
    if not user:
        console.print("[red]Error: USER environment variable is not set[/red]")
        sys.exit(1)

    # Check if it's a repo tool workspace
    manifest_file = work_dir / "manifest" / "default.xml"
    is_repo_workspace = manifest_file.exists()

    if is_repo_workspace:
        console.print("Building manifest project mapping...")
        project_paths = _load_manifest_project_paths(manifest_file)
        console.print(f"Manifest entries loaded: {len(project_paths)}")
    else:
        # Verify this is a single git repository
        result = subprocess.run(
            ["git", "-C", str(work_dir), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            console.print(f"[red]Error: Not a git repository or repo tool workspace: {work_dir}[/red]")
            sys.exit(1)

    console.print(f"Querying Gerrit for topic: {topic}")
    changes = _query_gerrit_ssh(topic, user, gerrit_server)

    total_changes = len(changes)
    successful_changes = 0
    failed_changes = 0

    if total_changes == 0:
        console.print(f"[yellow]No changes found for topic: {topic}[/yellow]")
        return

    console.print(f"Found {total_changes} change(s) in Gerrit.")

    for project, change_num, ref, subject in changes:
        console.print(f"\n[bold]Change #{change_num}: {subject}[/bold]")
        console.print(f"Project: {project}")

        if is_repo_workspace:
            # For repo workspace, find the project in manifest
            clean_project = project[:-4] if project.endswith(".git") else project
            local_path = project_paths.get(clean_project)

            if not local_path:
                console.print(
                    f"[yellow]No manifest entry for project: {project} (normalized: {clean_project}) -> skipping[/yellow]"
                )
                failed_changes += 1
                continue

            repo_dir = work_dir / local_path
            if not repo_dir.is_dir():
                console.print(f"[yellow]Repository path does not exist: {repo_dir} -> skipping[/yellow]")
                failed_changes += 1
                continue
        else:
            # For single git repo, use the work_dir directly
            repo_dir = work_dir

        if _checkout_change(repo_dir, project, ref, user, gerrit_server):
            successful_changes += 1
        else:
            failed_changes += 1

    console.print("\n" + "=" * 40)
    console.print(f"Total Gerrit Changes : {total_changes}")
    console.print(f"Successful Checkouts : {successful_changes}")
    console.print(f"Failed Checkouts     : {failed_changes}")
    console.print("=" * 40)


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Fetch and checkout Gerrit changes related to a Topic into your local Git workspace"
    )
    parser.add_argument(
        "topic",
        help="Gerrit topic to fetch changes for"
    )
    parser.add_argument(
        "--gerrit-server",
        default=GERRIT_SERVER,
        help=f"Gerrit server hostname (default: {GERRIT_SERVER})"
    )
    parser.add_argument(
        "--repo",
        default=".",
        help="Git repository path (default: current directory)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    try:
        checkout(args.topic, cwd=args.repo, gerrit_server=args.gerrit_server)
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
