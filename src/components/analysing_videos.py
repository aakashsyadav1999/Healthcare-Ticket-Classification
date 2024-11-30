import boto3
import time
import json
import os
import sys
from src.logger import logging
from src.exceptions import CustomException
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


class AnalyseVideos:
    
    def __init__(self, bucket_name, video_name, video_path):
        self.bucket_name = bucket_name
        self.video_name = video_name
        self.video_path = video_path
        self.client = boto3.client('')
        self.logger.info("Initialised AnalyseVideos class")
        
    def upload_video(self):
        try:
            response = self.client.upload_file(self.video_path, self.bucket_name, self.video_name)
            self.logger.info("Video uploaded")
        except Exception as e:
            self.logger.error("Error while uploading video")
            raise CustomException("Error while uploading video")
        
    