import os
from pathlib import Path

# Define the root directory of the project
project_name = 'src'

# List of file paths to be created as part of the project structure
files_list = [
    f"{project_name}/__init__.py",  # src/__init__.py

    # Components module - Contains modular scripts for different pipeline stages
    f"{project_name}/Components/__init__.py",
    f"{project_name}/Components/1_Data_Ingestion.py",
    f"{project_name}/Components/2_Data_Validation.py",
    f"{project_name}/Components/3_Data_Transformation.py",
    f"{project_name}/Components/4_Data_Trainer.py",
    f"{project_name}/Components/5_Data_Evaluation.py",
    f"{project_name}/Components/6_Data_Pusher.py",

    # Configuration module - Handles database and cloud config
    f"{project_name}/Configuration/__init__.py",
    f"{project_name}/Configuration/Mongo_DB_Connection.py",
    f"{project_name}/Configuration/AWS_Connection.py",

    # Cloud storage handler
    f"{project_name}/Cloud_Storage/__init__.py",
    f"{project_name}/Cloud_Storage/AWS_Storage.py",

    # Data Access layer
    f"{project_name}/Data_Access/__init__.py",
    f"{project_name}/Data_Access/Project_1_Data.py",

    # Constants module (for storing constant values)
    f"{project_name}/Constants/__init__.py",

    # Entity module (for configuration and artifact data classes)
    f"{project_name}/Entity/__init__.py",
    f"{project_name}/Entity/Config_Entity.py",
    f"{project_name}/Entity/Artifact_Entity.py",
    f"{project_name}/Entity/Estimator.py",
    f"{project_name}/Entity/S3_Estimator.py",

    # Exception handling module
    f"{project_name}/Exception/__init__.py",

    # Logging module
    f"{project_name}/Logger/__init__.py",

    # Pipeline module (Training & Prediction pipelines)
    f"{project_name}/Pipeline/__init__.py",
    f"{project_name}/Pipeline/Training_Pipeline.py",
    f"{project_name}/Pipeline/Prediction_Pipeline.py",

    # Utility functions
    f"{project_name}/Utils/__init__.py",
    f"{project_name}/Utils/Main_Utils.py",

    # Root-level files
    "app.py",                  # Main application file
    "requirements.txt",        # Project dependencies
    "Dockerfile",              # Docker build file
    ".dockerignore",           # Files to ignore in Docker build
    "demo.py",                 # Sample script or test file
    "setup.py",                # Python package setup script
    "pyproject.toml",          # Alternative modern Python packaging file
    "Config/Model.yaml",       # Model configuration in YAML format
    "Config/Schema.yaml"       # Schema definition for data validation
]

# Loop through all the file paths
for filepath in files_list:
    filepath = Path(filepath)  # Convert to Path object for compatibility
    file_dir, file_name = os.path.split(filepath)  # Split into directory and file name

    # If the file is inside a directory, create the directory (if it doesn't exist)
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)

    # Check if file doesn't exist OR is empty
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        # Create the file (as empty for now)
        with open(filepath, 'w') as f:
            pass  # Just open and close to create an empty file
    else:
        # If file already exists and is not empty, notify
        print(f"File Already Exists at: {filepath}")
