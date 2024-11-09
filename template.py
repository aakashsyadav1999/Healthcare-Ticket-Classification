import os
import sys
import logging



name_of_project = 'Ticket Classification System'

list_of_files = [

    'src/comoponents/ticket_request.py',
    'src/components/classification_process.py',
    'src/components/sending_ticket_into_bucket.py',
    'src/components/creating_meeting_room.py',
    'src/components/medical_store.py',
    'src/exceptions/__init__.py',
    'src/logger/__init__.py',
    'src/constants/__init__.py',
    'src/entities/__init__.py',
    'src/entities/config.py',
    'src/utils/__init__.py',
    'src/utils/common.py',
    'app.py',
    'main.py',
    'project.toml',
    'requirements.txt',
    'README.md',
    'Dockerfile',
    'docker-compose.yml',
    '.env'    
]


# Create the directories and files
for filepath in list_of_files:

    # Create the directories and files
    filepath = os.path.join(os.getcwd(), filepath)
    print(filepath)
    filedir, filename = os.path.split(filepath)

    # Create the directories if they do not exist
    if not os.path.exists(filedir):
        os.makedirs(filedir)
    
    # Create the files if they do not exist
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    # Create the files if they do not exist
    if (not os.path.exists(filepath) or (os.path.exists(filepath) and input(f"{filename} already exists. Do you want to overwrite it? (y/n): ").lower() == "y")):
        with open(filepath, "w") as f:
            f.write("")

        logging.info(f"Created file: {filepath}")

    # Skip creating the file
    else:
        logging.info(f"Skipped creating file: {filepath}")

