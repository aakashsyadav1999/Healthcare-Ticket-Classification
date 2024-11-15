import os
import sys
from datetime import datetime
import boto3
import boto3.resources
import json
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.config import AWSConfig
from src.logger import logging
from src.utils.common import CommonUtils

# Class to handle the medical history of the patient
class MedicalHistory:
    # Initialize the class with the patient ID
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.client_resources = boto3.resource('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
        self.client = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
        self.aws_download_config = AWSConfig()
        self.common_utils = CommonUtils()
        
    # Upload the medical history files to the S3 bucket    
    def upload_medic_history(self,file, overwrite=True):
        
        try:
            patient_history = f"medical_history/{self.patient_id}"
            folder_jpg = f"{patient_history}/jpg"
            folder_pdf = f"{patient_history}/pdf"
            # Check if the folder exists in the bucket
            logging.info(f"Checking if folder {patient_history} exists in the bucket {self.aws_download_config.aws_bucket}")
            bucket = self.client_resources.Bucket(self.aws_download_config.aws_bucket)
            logging.info(f"Bucket {self.aws_download_config.aws_bucket} found.")
            folder_exists = any(
                obj.key == patient_history for obj in bucket.objects.filter(Prefix=patient_history))
            
            if not folder_exists:
                logging.info(f"Folder {patient_history} does not exist. Creating folder.")
                # Create an empty object to create the folder
                self.client.put_object(Bucket=self.aws_download_config.aws_bucket, Key=(patient_history + '/'))
                
                logging.info(f"Folder {patient_history} created successfully.")
            else:
                logging.info(f"Folder {patient_history} already exists.")
                
            # Upload the files
            if overwrite:
                logging.info("Overwriting existing files.")
                # Delete all files in the folder
                for obj in bucket.objects.filter(Prefix=patient_history):
                    logging.info(f"Deleting file {obj.key}")
                    self.client.delete_object(Bucket=self.aws_download_config.aws_bucket, Key=obj.key)
                    logging.info(f"File {obj.key} deleted successfully.")
            else:
                logging.info("Not overwriting existing files.")
              
            logging.info("Uploading files.")  
            for file_type, file_path in file.items():
                if file_path:
                    if file_type == "jpg":
                        folder = folder_jpg
                    elif file_type == "pdf":
                        folder = folder_pdf
                    else:
                        logging.error(f"Invalid file type: {file_type}")
                        continue
                    
                    file_name = os.path.basename(file_path)
                    key = f"{folder}/{file_name}"
                    logging.info(f"Uploading file {file_name} to {key}")
                    self.client.upload_file(file_path, self.aws_download_config.aws_bucket, key)
                    logging.info(f"File {file_name} uploaded successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
        
    # Get all the URLs of the objects in the bucket
    def get_all_object_urls(self):
            try:
                patient_history = f"medical_history/{self.patient_id}"
                urls = {"patient_id":self.patient_id,"jpg": [], "pdf": []}
                
                for file_type in urls.keys():
                    folder = f"{patient_history}/{file_type}"
                    bucket = self.client_resources.Bucket(self.aws_download_config.aws_bucket)
                    
                    for obj in bucket.objects.filter(Prefix=folder):
                        if obj.key.endswith(file_type):
                            url = f"https://{self.aws_download_config.aws_bucket}.s3.amazonaws.com/{obj.key}"
                            urls[file_type].append(url)
                return urls
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                return None
    
    # Insert the URLs into the database
    def insert_into_db(self):
        
        try:
            response = self.get_all_object_urls()
            logging.info(f"URLs found: {response}")
            if response: 
                response["patient_id"] = self.patient_id     
                collection = self.common_utils.insert_into_video_table()
                collection.insert_one(response)
                logging.info(f"URL {response} inserted successfully.")  
            else:
                logging.error("No URLs found.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
                
    
if __name__ == "__main__":
    medical_history = MedicalHistory("1234")
    #medical_history.upload_medic_history({"jpg": r"D:\vscode\Healthcare-Ticket-Classification\download.jpg", "pdf": r"D:\vscode\Healthcare-Ticket-Classification\LastTenTransactions.pdf"})
    #print(medical_history.get_all_object_urls())
    medical_history.insert_into_db()