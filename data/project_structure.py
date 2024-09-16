import os
import subprocess
import pandas as pd
import logging

# Set up logging configuration
logging.basicConfig(
    filename='project_structure.log',  # Log to a file
    filemode='a',  # Append mode
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    level=logging.INFO  # Log level
)

def get_tree_output(root_dir):
    """Runs the 'tree' command in the parent directory of root_dir and returns the output, including hidden files."""
    try:
        # Compute the parent directory
        parent_dir = os.path.abspath(os.path.join(root_dir, '..'))
        
        # Execute the 'tree' command in the parent directory
        result = subprocess.run(['tree', '-afi', parent_dir], stdout=subprocess.PIPE, text=True)
        
        return result.stdout
    except Exception as e:
        logging.error(f"Error running 'tree' command: {e}")
        return None


def parse_tree_output(tree_output, root_dir):
    """Parses the output of the 'tree' command and returns a list of dictionaries for each file/directory."""
    lines = tree_output.splitlines()
    data = []
    summary = ""

    # Compute the parent directory path
    parent_dir = os.path.abspath(os.path.join(root_dir, '..'))

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

        # Compute the relative path with respect to the parent directory
        relative_path = os.path.relpath(file_path, parent_dir)
        
        # Get the directory name where the entity is located
        directory_name = os.path.basename(os.path.dirname(file_path))
        
        # Determine if the path is a directory or a file
        is_directory = os.path.isdir(file_path)

        # Store the info
        data.append({
            "directory_name": directory_name,  # Name of the directory containing the entity
            "entity_name": os.path.basename(file_path),
            "relative_path": relative_path,
            "level": relative_path.count(os.path.sep),  # Level relative to the parent directory
            "type": "directory" if is_directory else "file"
        })

    return data, summary


def generate_project_dataset(root_dir):
    """Generates a dataset of the project structure and saves it to a pickle file."""
    tree_output = get_tree_output(root_dir)
    
    if not tree_output:
        logging.warning(f"Could not get tree output for the root directory: {root_dir}")
        return
    
    # Parse the output
    data, summary = parse_tree_output(tree_output, root_dir)

    # Create a DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to a pickle file
    output_path = os.path.join(root_dir, '../', 'data', 'project_structure.pkl')
    try:
        df.to_pickle(output_path)
        logging.info(f"DataFrame saved to {output_path}")
    except Exception as e:
        logging.error(f"Error saving DataFrame to pickle file: {e}")
    
    # Log the summary line
    if summary:
        logging.info(f"Summary: {summary}")

if __name__ == "__main__":
    # Replace '.' with your project root directory if necessary
    root_directory = os.path.abspath(os.path.dirname(__file__))
    generate_project_dataset(root_directory)