import os
import sys
import pandas as pd
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
import google.generativeai as genai
import json

# Ensure the src directory is in the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.entities.config import GeminiConfig
from src.logger import logging
from src.exceptions import CustomException
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv

# Load the environment variables
load_dotenv(find_dotenv())
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#TODO : Create ENUM classification input feeling ticks for predicting the feeling of the user
class FeelingTicks(str,Enum):
    VERY_BAD = 0
    BAD = 1
    NEUTRAL = 2
    GOOD = 3
    VERY_GOOD = 4
    
class ClinicalSupport(str,Enum):
    Medical_ADVICE = 0
    PSYCHOLOGICAL_ADVICE = 1
    PRESCRIPTION_ADVICE = 2
    TEST_RESULT = 3
    APPOINTMENT_SCHEDULING = 4
    SPECIALIST_CONSULTATION = 5
    
class PatientCareCorrdinator(str,Enum):
    MEDICAL_TRANSPORT = 0
    MEDICAL_APPOINTMENT = 1
    REFERRAL_MANAGEMENT = 2
    FOLLOW_UP_CARE = 3
    CARE_PLAN_ADJUSTMENT = 4
    HOME_HEALTH_CARE = 5
    PAITENT_TRANSPORT_SERVICES = 6
    
#TODO: Create using pydantic basemodel for the input data for the classification process
class ClassificationInput(BaseModel):
    patient_id: int
    feeling: FeelingTicks
    clinical_support: ClinicalSupport
    patient_care_coordinator: PatientCareCorrdinator
    created_at: datetime = datetime.now()
    confidence: float = Field(ge=0, le=1, description="Confidence score for the classification")
    key_information: List[str] = Field(description="List of key points extracted from the ticket")
    suggested_action: str = Field(description="Brief suggestion for handling the ticket")
    
#Example ticket for the classification process
ticket_1 = {
    "patient_id": '123',
    "ticket": 'I am feeling very bad and need medical advice. I also need medical transport to the hospital.'
}
ticket_2 = {
    "patient_id": 456,
    "ticket": 'I am feeling dizzy, I think I have catched cold and I am having running nose.'
}

class Gemini:
    
    def __init__(self):
        
        self.google_api = GeminiConfig()
        
    def mongo_connection(self):
            mongo_host = os.getenv("MONGODB_URI")
            mongo_port = int(os.getenv("MONGODB_PORT"))
            mongo_db = os.getenv("MONGODB")
            mongo_collection = os.getenv("MONGO_COLLECTION")
            client = MongoClient(mongo_host, mongo_port)
            db = client[mongo_db]
            collection = db[mongo_collection]
            return collection
        

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
            logging.error(f"Error in gemini api: {str(e)}")
            return f"Error: {str(e)}"

    #TODO: Apply Gemini flash 1.5 process for the classification process
    def classify_ticket(self, ticket: str) -> ClassificationInput:
        """
        Function to classify the ticket
        """
        logging.info(f"Classifying ticket: {ticket}")
        model = self.gemini_api()  # Ensure this correctly initializes the model

        prompt = f"""You are an expert in health care sector for ticket classification customer support team.
                    Your role is to analyze incoming customer support tickets and provide structured information to help our team respond quickly and effectively.
                    Ticket: {ticket}"""

        # Use the appropriate method for generating a response
        response = model.generate_content(prompt,generation_config={"response_mime_type": "application/json"})  # Replace 'generate' with the correct method if needed
        logging.info(f"Response from Gemini: {response.text}")
        response = json.loads(response.text)
        return response


#TODO: Insert that data into database matching on patient id column
    def insert_into_database(self,ticket):
        """
        Function to insert the response into the database
        """
        try:
            response = self.classify_ticket(ticket["ticket"])
            response["patient_id"] = str(ticket["patient_id"])
            # Log types of each key and value
            for key, value in response.items():
                logging.info(f"Key: {key}, Type: {type(key)}, Value: {value}, Value Type: {type(value)}")
            # Ensure all keys and values are strings where required
            response = {str(key): str(value) if not isinstance(value, (str, list)) else value for key, value in response.items()}
            response = {key.replace("$", "_").replace(".", "_"): value for key, value in response.items()}
            logging.info(f"Response to be inserted into database: {response}")
            collection = self.mongo_connection()
            collection.insert_one(response)
            logging.info(f"Response inserted into database: {response}")
        except Exception as e:
            logging.error(f"Error in inserting into database: {str(e)}")
            return f"Error: {str(e)}"

#TODO: Mark ticket into the database as processed
    # def mark_ticket_as_processed(self, ticket_id: str):
    #     """
    #     Function to mark the ticket as processed
    #     """
    #     try:
    #         collection = self.mongo_connection()
    #         collection.update_one({"ticket_id": ticket_id}, {"$set": {"processed": True}})
    #         logging.info(f"Ticket with ID {ticket_id} marked as processed")
    #     except Exception as e:
    #         logging.error(f"Error in marking ticket as processed: {str(e)}")
    #         return f"Error: {str(e)}"
        
    def initiate_classification_process(self):
        """
        Function to initiate the classification process
        """
        try:
            ticket = ticket_1
            #self.mongo_connection()
            #self.classify_ticket(ticket['ticket'])
            self.insert_into_database(ticket)
            
        except Exception as e:
            logging.error(f"Error in classification process: {str(e)}")
            return f"Error: {str(e)}"
        

if __name__ == "__main__":
    gemini = Gemini()
    gemini.initiate_classification_process()