import boto3
import time
import json
import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.logger import logging
from src.exceptions import CustomException
from src.utils.common import CommonUtils
from src.entities.config import GeminiConfig, AWSConfig
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class AnalyseVideos:
    
    def __init__(self, video_path):
        self.video_path = video_path
        self.google_api = GeminiConfig()
        self.bucket_name = AWSConfig().aws_bucket
        self.client_resources = boto3.resource('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
        logging.info("S3 client resources created")
        self.client = boto3.client('s3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
            aws_secret_access_key=os.getenv('AWS_SECRET_KEY'))
    
    #Gemini API
    def gemini_api(self):
        """
        Apply gemini api and call it later in prompt section with image input for response.
        """
        try:
            
            self.gemini_api_obj = self.google_api.gemini_api  #get api key from google api     
            genai.configure(api_key=self.gemini_api_obj)     #configure the api key
            gemini_model = genai.GenerativeModel(self.google_api.gemini_model) #get the model name from google api
            logging.info(f"Gemini model configured: {gemini_model}")
            return gemini_model
        except Exception as e:
            logging.error("Error while configuring gemini model")
            raise (f"Error while configuring gemini model {e}")
    
    #Paient ID
    def patient_id(self):
        try:
            patient_id = input("Enter the patient id: ")
            return patient_id
        except Exception as e:
            logging.error("Error while extracting patient id")
            raise CustomException(f"Error while extracting patient id {e}")
    
    #Upload video to S3 bucket
    def upload_video(self):
        try:
            patient_id = "0000"
            print(patient_id)
            video_folder = f"medical_history/{patient_id}/videos"
            bucket = self.client_resources.Bucket(self.bucket_name)
            print(bucket)
            folder_exists = any(obj.key == video_folder for obj in bucket.objects.filter(Prefix=video_folder))
            
            if not folder_exists:
                logging.info(f"Folder {video_folder} does not exist. Creating folder.")
                self.client.put_object(Bucket=self.bucket_name, Key=f"{video_folder}/")
                logging.info(f"Folder {video_folder} created successfully.")
            else:
                logging.info(f"Folder {video_folder} already exists.")
            key = f"medical_history/{patient_id}/videos/{os.path.basename(self.video_path)}"
            self.client_resources.Bucket(self.bucket_name).upload_file(self.video_path, key)
            logging.info(f"Video uploaded to {key}")
        except Exception as e:
            logging.error("Error while uploading video")
            raise CustomException(f"Error while uploading video {e}")

    #Get video name
    def get_url(self):
        try:
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{self.video_name}"
            logging.info("Video url generated")
            return url
        except Exception as e:
            logging.error("Error while generating video url")
            raise CustomException(f"Error while generating video url {e}")
        
    def analyse_video(self):
        try:
            model = self.gemini_api()
            prompt = f"Analyse the video {self.get_url()}"
            response = model.generate_content(prompt, max_length=1000)
            logging.info("Video analysis started")
            return response
        except Exception as e:
            logging.error("Error while analysing video")
            raise CustomException("Error while analysing video")
    
    def insert_into_database(self):
        
        try:
            response = self.analyse_video()
            patient_id = self.patient_id()
            response["patient_id"] = patient_id
            response = {str(key): str(value) if not isinstance(value, (str, list)) else value for key, value in response.items()}
            response = {key.replace("$", "_").replace(".", "_"): value for key, value in response.items()}
            collection = self.common_utils.insert_main_table()
            collection.insert_one(response)
            logging.info("Response inserted into database")
        except Exception as e:
            logging.error("Error while inserting response into database")
            raise CustomException("Error while inserting response into database")

    #Main function
    def main(self):
        try:
            self.upload_video()
            #self.insert_into_database()
            logging.error("Video analysis completed")
        except Exception as e:
            logging.error("Error while analysing video")
            raise CustomException(f"Error while analysing video {e}")
        
if __name__ == "__main__":
    video_path = r'D:\vscode\Healthcare-Ticket-Classification\12731602_2160_3840_60fps.mp4'
    AnalyseVideos(video_path).main()
    