# scripts\update_readme_project_info.py
from __future__ import annotations

import os
import threading
import time
from datetime import datetime
from typing import Any

import pytz  # type: ignore

from sanruum.config import BaseConfig

README_FILE = os.path.join(BaseConfig.BASE_DIR, 'STATS.md')

# Define the inactivity threshold in seconds (5 minutes)
INACTIVITY_THRESHOLD = 5 * 60  # 5 minutes

# Initialize last modified timestamp to track file changes
last_modified_time: float = 0.0
time_spent_working: float = 0.0  # Ensure float for division operations
last_activity_time = time.time()


def get_project_info(base_dir: Any) -> dict[str, int | str]:
    # Initialize data
    total_size = 0
    total_lines = 0
    editable_files = 0
    total_files = 0

    # Walk through the directory and gather data
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            filepath = os.path.join(root, file)
            total_files += 1
            total_size += os.path.getsize(filepath)

            # Count lines of code for Python files
            if file.endswith('.py'):
                editable_files += 1
                with open(filepath, encoding='utf-8') as f:
                    total_lines += len(f.readlines())

    # Get the current time in Europe/Tallinn timezone
    tz = pytz.timezone('Europe/Tallinn')
    last_updated = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    # Prepare the project info
    return {
        'total_size': total_size,  # Ensure int type
        'total_lines': total_lines,  # Ensure int type
        'total_files': total_files,  # Ensure int type
        'editable_files': editable_files,  # Ensure int type
        'last_updated': last_updated,  # String
    }


def update_readme_with_project_info() -> None:
    global last_modified_time, time_spent_working, last_activity_time

    # Get project info and update README
    project_info = get_project_info(BaseConfig.BASE_DIR)

    total_size_mb = int(project_info['total_size']) / (1024 * 1024)

    # Prepare the new content for README.md
    new_content = f"""
# Project Overview

- **Last Updated**: {project_info['last_updated']}
- **Total Project Size**: {total_size_mb:.2f} MB
- **Editable Files (Python)**: {project_info['editable_files']}
- **Total Lines of Code (LOC)**: {project_info['total_lines']}
- **Total Files**: {project_info['total_files']}

---

## Progress Summary
This is an ongoing project with development and testing stages.
    Current progress is as follows:
- In Progress: {project_info['editable_files']} files being
    actively worked on.
- Last major update: {project_info['last_updated']}

---

## Time Tracking
- **Total Time Spent**: {time_spent_working / 3600:.2f} hours
- **Average Daily Working Time**: {time_spent_working / (3600 * 7):.2f} hours
    (based on a 7-day work week)
"""

    # Check if README.md exists and update it
    if os.path.exists(README_FILE):
        with open(README_FILE, encoding='utf-8') as file:
            content = file.read()

        # If content is different, update the README file
        if new_content.strip() != content.strip():
            with open(README_FILE, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print('README.md updated.')
        else:
            print('README.md is already up-to-date.')
    else:
        # If README.md doesn't exist, create it
        with open(README_FILE, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print('README.md created.')

    # Track time spent working
    current_time = time.time()
    time_spent_working += current_time - last_activity_time
    last_activity_time = current_time


def monitor_for_changes() -> None:
    global last_modified_time

    while True:
        current_time = time.time()

        # Monitor file changes in the BASE_DIR
        for root, dirs, files in os.walk(BaseConfig.BASE_DIR):
            for file in files:
                filepath = os.path.join(root, file)
                file_modified_time = os.path.getmtime(filepath)

                if file_modified_time > last_modified_time:
                    last_modified_time = file_modified_time
                    # Update README if changes detected
                    update_readme_with_project_info()

        # Check for inactivity (if no changes for a set threshold)
        if current_time - last_activity_time > INACTIVITY_THRESHOLD:
            print('No activity detected, stopping time tracking.')
            break

        # Sleep for a while before checking again
        time.sleep(30)


def start_background_task() -> None:
    # Start the monitoring task in a separate thread to keep it running in the
    # background
    background_thread = threading.Thread(target=monitor_for_changes)
    # This makes the thread exit when the main program exits
    background_thread.daemon = True
    background_thread.start()


if __name__ == '__main__':
    start_background_task()

    # Main program logic (could be a server or any other process)
    print('Project Tracker is running in the background...')
    while True:
        time.sleep(1000)  # Keep the main program running
