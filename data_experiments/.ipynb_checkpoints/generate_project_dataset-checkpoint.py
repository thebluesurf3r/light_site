import os
import subprocess
import pandas as pd

def get_tree_output(root_dir):
    """Runs the 'tree' command in the root directory and returns the output, including hidden files."""
    try:
        result = subprocess.run(['tree', '-afi', root_dir], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return None

def parse_tree_output(tree_output, root_dir):
    """Parses the output of the 'tree' command and returns a list of dictionaries for each file/directory."""
    lines = tree_output.splitlines()
    data = []
    summary = ""

    for line in lines:
        # Capture the summary line
        if 'directories' in line and 'files' in line:
            summary = line.strip()
            continue
        
        # Skip empty lines and tree summary lines that we have already captured
        if not line.strip() or line == summary:
            continue

        # Get the absolute path of the file/folder
        file_path = line.strip()
        if not os.path.isfile(file_path) and not os.path.isdir(file_path):
            continue

        # Compute the relative path
        relative_path = os.path.relpath(file_path, root_dir)
        
        # Determine the app name
        app_name = root_dir.split(os.path.sep)[-1]  # Using the project root name for app_name
        
        # Check if it's a directory or a file
        is_directory = os.path.isdir(file_path)

        # Store the info
        data.append({
            "app_name": app_name,
            "file_name": os.path.basename(file_path),
            "relative_path": relative_path,
            "level": relative_path.count(os.path.sep),
            "type": "directory" if is_directory else "file"
        })

    return data, summary

def generate_project_dataset(root_dir):
    """Generates a dataset of the project structure and saves it to a pickle file."""
    tree_output = get_tree_output(root_dir)
    
    if not tree_output:
        print(f"Could not get tree output for the root directory.")
        return
    
    # Parse the output
    data, summary = parse_tree_output(tree_output, root_dir)

    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to a pickle file
    df.to_pickle(os.path.join(root_dir, 'data', 'project_structure.pkl'))
    print(f"DataFrame saved to {os.path.join(root_dir, 'data', 'project_structure.pkl')}")
    
    # Print summary line
    if summary:
        print(f"\nSummary:\n{summary}")

if __name__ == "__main__":
    # Replace '.' with your project root directory if necessary
    root_directory = os.path.abspath(os.path.dirname(__file__))
    generate_project_dataset(root_directory)
