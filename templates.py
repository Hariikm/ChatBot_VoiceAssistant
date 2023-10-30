import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format= '[%(asctime)s]: %(message)s:')

project_name = "Thrisha_Assistant"

list_of_files = [

    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    "settings.yaml",
    "requirements.txt",
    "personality.txt",
    "setup.py",
    "research/trials.ipynb",
    "main.py"
]

for filepath in list_of_files:
    filepath = Path(filepath)

    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir, exist_ok= True)
        logging.info(f"Created directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)== 0):
        with open(filepath, 'w') as f:
            pass # creating an empty file
            logging.info(f"Creating empty file: {filepath}")

    else:
        logging.info(f"{filename} already exist")    
