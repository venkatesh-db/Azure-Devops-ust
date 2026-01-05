# Script to Generate Automated Release Notes

import datetime
import os
import subprocess

def fetch_git_changes():
    """
    Fetch the latest Git commit messages as changes.

    Returns:
        list: List of commit messages.
    """
    try:
        result = subprocess.run(["git", "log", "--pretty=format:%s", "-n", "10"], capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Error fetching Git changes: {e}")
        return []

def generate_release_notes(changes, version):
    """
    Generate release notes based on the provided changes and version.

    Args:
        changes (list): List of changes in the release.
        version (str): Version of the release.

    Returns:
        str: Formatted release notes.
    """
    release_date = datetime.date.today().strftime("%B %d, %Y")
    notes = f"Release Notes - Version {version} ({release_date})\n"
    notes += "\nChanges:\n"
    for change in changes:
        notes += f"- {change}\n"
    return notes

def save_release_notes(notes, output_dir="release_notes"):
    """
    Save the release notes to a file.

    Args:
        notes (str): The release notes content.
        output_dir (str): Directory to save the release notes file.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    file_path = os.path.join(output_dir, f"release_notes_{datetime.date.today()}.txt")
    with open(file_path, "w") as file:
        file.write(notes)
    print(f"Release notes saved to {file_path}")

# Example usage
if __name__ == "__main__":
    version = "1.0.0"  # Replace with actual version
    changes = fetch_git_changes()
    if not changes:
        changes = ["No significant changes recorded."]
    release_notes = generate_release_notes(changes, version)
    save_release_notes(release_notes)