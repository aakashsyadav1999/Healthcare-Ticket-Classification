import os
import sys
from src.constants import *
from src.logger import logging
from src.exceptions import CustomException
from dataclasses import dataclass
from dotenv import load_dotenv, find_dotenv


@dataclass
class GeminiConfig:
    """
    Class to hold the
    configuration for the Gemini
    application
    """
    def __init__(self):
        
        self.gemini_api = GEMINI_API_KEY
        self.gemini_model = GEMINI_MODEL
        
    
@dataclass
class AWSConfig:
    """
    Class to hold the
    configuration for the AWS
    S3 bucket
    """
    def __init__(self):
        
        self.aws_access_key = AWS_ACCESS_KEY
        self.aws_secret_key = AWS_SECRET_KEY
        self.aws_bucket = AWS_BUCKET  