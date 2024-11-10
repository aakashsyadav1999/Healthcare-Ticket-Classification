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
        
    
    