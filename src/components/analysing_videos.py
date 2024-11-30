import boto3
import time
import json
import os
import sys
from src.logger import logging
from src.exceptions import CustomException
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from src.utils.common import CommonUtils
from src.entities.config import GeminiConfig
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class AnalyseVideos:
    
    def __init__(self, bucket_name, video_name, video_path):
        self.bucket_name = bucket_name
        self.video_name = video_name
        self.video_path = video_path
        self.logger.info("Initialised AnalyseVideos class")
        self.google_api = GeminiConfig()
        
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
            self.logger.error("Error while configuring gemini model")
            raise CustomException("Error while configuring gemini model")
    
    
    def patient_id(self):
        try:
            patient_id = input("Enter the patient id: ")
            return patient_id
        except Exception as e:
            self.logger.error("Error while extracting patient id")
            raise CustomException("Error while extracting patient id")
    
    def upload_video(self):
        try:
            response = self.client.upload_file(self.video_path, self.bucket_name, self.video_name)
            self.logger.info("Video uploaded")
        except Exception as e:
            self.logger.error("Error while uploading video")
            raise CustomException("Error while uploading video")
        
    def get_url(self):
        try:
            url = f"https://{self.bucket_name}.s3.amazonaws.com/{self.video_name}"
            self.logger.info("Video url generated")
            return url
        except Exception as e:
            self.logger.error("Error while generating video url")
            raise CustomException("Error while generating video url")
        
    def analyse_video(self):
        try:
            model = self.gemini_api()
            prompt = f"Analyse the video {self.get_url()}"
            response = model.generate_content(prompt, max_length=1000)
            self.logger.info("Video analysis started")
            return response
        except Exception as e:
            self.logger.error("Error while analysing video")
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
            self.logger.info("Response inserted into database")
        except Exception as e:
            self.logger.error("Error while inserting response into database")
            raise CustomException("Error while inserting response into database")
        
    def main(self):
        try:
            self.upload_video()
            self.insert_into_database()
            self.logger.info("Video analysis completed")
        except Exception as e:
            self.logger.error("Error while analysing video")
            raise CustomException("Error while analysing video")
        
if __name__ == "__main__":
    bucket_name = input("Enter the bucket name: ")
    video_name = input("Enter the video name: ")
    video_path = input("Enter the video path: ")
    analyse_videos = AnalyseVideos(bucket_name, video_name, video_path)
    analyse_videos.main()