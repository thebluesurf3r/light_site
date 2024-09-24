import pickle
import os
import pandas as pd
from .models import ProjectEntity

def load_data():
    # Load the pickle file into a DataFrame
    file_name = 'structure_processed.pkl'
    pickle_file_path = os.path.join(os.path.expanduser('~'), 'git', 'light_site', 'media', 'project_structure', file_name)
    df = pd.read_pickle(pickle_file_path)
    
    # Iterate through the DataFrame and insert data into the database
    for _, row in df.iterrows():
        ProjectEntity.objects.create(
            directory=row['directory'],
            filename=row['filename'],
            full_path=row['full_path'],
            file_size=row['file_size'],
            metadata_change_time=row['metadata_change_time'],
            modification_time=row['modification_time'],
            access_time=row['access_time'],
            file_age_in_days=row['file_age_in_days'],
            meta_data_age_in_days=row['meta_data_age_in_days'],
            recently_accessed=row['recently_accessed'],
            file_size_category=row['file_size_category'],
            file_extension=row['file_extension'],
            python_file=row['python_file'],
            file_depth=row['file_depth'],
            django_element_type=row['django_element_type'],
            expected_location=row['expected_location'],
            hover_template=row['hover_template']
        )

    print("Data successfully loaded into the database.")
