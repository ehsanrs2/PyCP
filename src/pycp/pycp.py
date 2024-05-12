#!/usr/bin/env python3
import sys
import subprocess
import argparse
from pathlib import Path
import time


def install_package(package_name):
    """Ensures the required Python package is installed."""
    try:
        __import__(package_name)
    except ImportError:
        response = input(f"The required package '{package_name}' is not installed. Install it now? (y/n): ").lower()
        if response in ['y', 'yes']:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        else:
            print("This script cannot run without the necessary packages. Exiting.")
            sys.exit(1)


install_package('rich')  # Ensure the 'rich' package is installed

from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn


def create_progress_bar():
    """Creates and returns a configured Rich progress bar object."""
    return Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeRemainingColumn(),
        transient=True
    )


def format_speed(bytes_per_sec):
    """Formats speed from bytes per second to a readable string.
    Arg:
        bytes_per_sec: Number of bytes per second
    Returns:
        Readable string representation of the speed
    """
    if bytes_per_sec < 1024:
        return f"{bytes_per_sec:.2f} B/s"
    elif bytes_per_sec < 1024**2:
        return f"{bytes_per_sec / 1024:.2f} KB/s"
    else:
        return f"{bytes_per_sec / 1024**2:.2f} MB/s"


def copy_file_with_progress(src, dest, progress, total_task, current_task, start_time, total_transferred, overwrite):
    """Copies a single file and updates the progress bars for individual file progress and total progress.
    Arg:
        src: Path to the source file
        dest: Path to the destination file
        progress: Rich Progress object
        total_task: Task ID for the total progress bar
        current_task: Task ID for the current file progress bar
        start_time: Time when the copying operation started
        total_transferred: Total number of bytes transferred so far
        overwrite: Whether to overwrite existing files without asking
    Returns:
        Number of bytes transferred
    """
    src = Path(src)
    dest = Path(dest)

    if not overwrite and dest.exists():
        print(f"Skipping {src} because it already exists.")
        return 0  # Skip this file

    transferred = 0
    with src.open('rb') as f_src, dest.open('wb') as f_dest:
        while chunk := f_src.read(4096):
            f_dest.write(chunk)
            transferred += len(chunk)
            total_transferred += len(chunk)
            progress.update(current_task, advance=len(chunk))
            progress.update(total_task, advance=len(chunk))
            elapsed_time = time.time() - start_time
            if elapsed_time > 0:
                speed = total_transferred / elapsed_time
                progress.update(total_task, description=f"Total Progress ({format_speed(speed)}):")
    return transferred


def copy_directory_recursive(src, dest, progress, total_task, start_time, total_transferred, overwrite):
    """Recursively copies directories and files, updating the progress bar.
    Arg:
        src: Path to the source directory
        dest: Path to the destination directory
        progress: Rich Progress object
        total_task: Task ID for the total progress bar
        start_time: Time when the copying operation started
        total_transferred: Total number of bytes transferred so far
        overwrite: Whether to overwrite existing files without asking
    Returns:
        Total number of bytes transferred
    """
    src_path = Path(src)
    dest_path = Path(dest)
    dest_path.mkdir(exist_ok=True)

    for item in src_path.iterdir():
        source_item = src_path / item.name
        dest_item = dest_path / item.name
        if source_item.is_dir():
            total_transferred = copy_directory_recursive(source_item, dest_item, progress, total_task, start_time,
                                                         total_transferred, overwrite)
        else:
            current_task = progress.add_task(f"Copying {source_item.name}", total=source_item.stat().st_size)
            total_transferred += copy_file_with_progress(source_item, dest_item, progress, total_task, current_task,
                                                         start_time, total_transferred, overwrite)
            progress.remove_task(current_task)
    return total_transferred


def main():
    """Handles command line arguments and orchestrates file copying operations."""
    parser = argparse.ArgumentParser(description="Copy files and directories with a progress bar.")
    parser.add_argument('source', type=str, help='Source file or directory to copy')
    parser.add_argument('destination', type=str, help='Destination path')
    parser.add_argument('-r', '--recursive', action='store_true', help='Copy directories recursively')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite existing files without asking')
    args = parser.parse_args()

    src = Path(args.source)
    dest = Path(args.destination)
    if not src.exists():
        print(f"The source {src} does not exist.")
        sys.exit(1)
    if not dest.exists():
        dest.mkdir(parents=True, exist_ok=True)

    progress = create_progress_bar()
    start_time = time.time()
    total_transferred = 0
    with progress:
        total_size = sum(f.stat().st_size for f in src.rglob('*') if f.is_file()) if args.recursive else src.stat().st_size
        total_task = progress.add_task("Copying files...", total=total_size)
        total_transferred = copy_directory_recursive(src, dest, progress, total_task, start_time, total_transferred, args.overwrite)

    print("All files copied successfully.")


if __name__ == "__main__":
    main()
