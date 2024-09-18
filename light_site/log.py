import ast
import os
import re

# Define substrings or patterns for exclusion
EXCLUSION_PATTERNS = [
    'pip._internal', 'pip._vendor', '__', '_', 'pkg_resources'
]

def is_excluded(module_name):
    """
    Check if the module name matches any of the exclusion patterns.
    
    :param module_name: Name of the module to check
    :return: True if the module is excluded, False otherwise
    """
    return any(pattern in module_name for pattern in EXCLUSION_PATTERNS)

def log_imported_libraries(project_dir):
    """
    Scan the project directory for all Python files and log unique import statements.
    
    :param project_dir: Path to the project directory
    """
    unique_imports = set()
    
    # Traverse the project directory
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith('.py'):
                base_dir = os.path.join(root, file)
                with open(base_dir, 'r', encoding='utf-8') as f:
                    try:
                        # Parse the file's AST
                        tree = ast.parse(f.read(), filename=base_dir)
                        # Extract import statements
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    if alias.name is not None and not is_excluded(alias.name):
                                        unique_imports.add(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                if node.module is not None and not is_excluded(node.module):
                                    unique_imports.add(node.module)
                    except SyntaxError as e:
                        print(f"Syntax error in file {base_dir}: {e}")
    
    # Log unique imports
    if unique_imports:
        print("Unique imports across the project:")
        for imp in sorted(unique_imports):
            print(imp)
        print(f"\nTotal unique modules: {len(unique_imports)}")
    else:
        print("No unique modules found.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python log.py <project_dir>")
        sys.exit(1)
    project_dir = sys.argv[1]
    log_imported_libraries(project_dir)