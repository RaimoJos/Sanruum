# scripts\add_filename.py
import os

from sanruum.constants import BASE_DIR


def add_filename_to_file(filepath):
    # Get the relative path from BASE_DIR
    relative_path = os.path.relpath(filepath, BASE_DIR)

    # Prepare the comment to be added
    new_comment = f"# {relative_path}\n"

    # Open the file and read its contents
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Check if the first line already contains a comment with the filename
    if content and content[0].startswith("#"):
        if content[0].strip() != new_comment.strip():  # If the comment is different, add it
            content.insert(0, new_comment)  # Insert the new comment at the top
            print(f"Comment added to: {filepath}")
        else:
            print(f"Comment already exists in: {filepath}")
    else:
        # Insert the new comment at the top of the file
        content.insert(0, new_comment)
        print(f"Comment added to: {filepath}")

    # Write the modified content back to the file
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(content)


def add_comments_to_all_python_files(base_dir):
    # Walk through the directory and process each Python file
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):  # Check for Python files
                filepath = os.path.join(root, file)
                add_filename_to_file(filepath)


# Run the function to process all Python files in the specified directory
add_comments_to_all_python_files(BASE_DIR)
