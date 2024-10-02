import os

def create_file(filepath):
    """Creates an empty file at the specified path."""
    with open(filepath, 'w') as file:
        pass

def create_dir_structure():
    # Root app directory
    app_dir = 'dir_scan'
    os.makedirs(app_dir, exist_ok=True)
    
    # Create base files
    #base_files = ['admin.py', 'apps.py', '__init__.py', 'models.py', 'urls.py']
    #for file in base_files:
    #    create_file(os.path.join(app_dir, file))
    
    # Create migrations directory
    migrations_dir = os.path.join(app_dir, 'migrations')
    os.makedirs(migrations_dir, exist_ok=True)
    create_file(os.path.join(migrations_dir, '0001_initial.py'))
    create_file(os.path.join(migrations_dir, '__init__.py'))

    # Create project_scanner directory and files
    project_scanner_dir = os.path.join(app_dir, 'project_scanner')
    os.makedirs(project_scanner_dir, exist_ok=True)
    project_scanner_files = ['project_structure_validator.py', 'directory_scanner.py', 'file_categorizer.py']
    for file in project_scanner_files:
        create_file(os.path.join(project_scanner_dir, file))
    
    # Create data_preprocessing directory and files
    data_preprocessing_dir = os.path.join(app_dir, 'data_preprocessing')
    os.makedirs(data_preprocessing_dir, exist_ok=True)
    data_preprocessing_files = ['raw_data_extractor.py', 'feature_engineering.py', 'data_cleaning.py', 'dataset_aggregator.py']
    for file in data_preprocessing_files:
        create_file(os.path.join(data_preprocessing_dir, file))
    
    # Create visualization_utils directory and files
    visualization_utils_dir = os.path.join(app_dir, 'visualization_utils')
    os.makedirs(visualization_utils_dir, exist_ok=True)
    visualization_utils_files = ['plotly_helpers.py', 'custom_tooltips.py', 'color_map_generator.py']
    for file in visualization_utils_files:
        create_file(os.path.join(visualization_utils_dir, file))
    
    # Create data_export directory and files
    data_export_dir = os.path.join(app_dir, 'data_export')
    os.makedirs(data_export_dir, exist_ok=True)
    data_export_files = ['db_pusher.py', 'csv_exporter.py']
    for file in data_export_files:
        create_file(os.path.join(data_export_dir, file))

    # Create display_utils directory and files
    display_utils_dir = os.path.join(app_dir, 'display_utils')
    os.makedirs(display_utils_dir, exist_ok=True)
    display_utils_files = ['dataframe_html_renderer.py', 'dataframe_printer.py']
    for file in display_utils_files:
        create_file(os.path.join(display_utils_dir, file))
    
    print("Project structure created successfully!")

if __name__ == "__main__":
    create_dir_structure()
