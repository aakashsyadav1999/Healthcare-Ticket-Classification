import pandas as pd
import numpy as np


class MedicalStore:
    def __init__(self, name, inventory, rating, location, home_delivery):
        self.name = name  # Name of the medical store
        self.inventory = inventory  # List of medicines available in the store
        self.rating = rating  # Rating of the store
        self.location = location  # Location of the store [latitude, longitude]
        self.home_delivery = home_delivery  # Whether the store offers home delivery

    def get_inventory(self):
        return self.inventory

    def get_inventory_df(self):
        # Convert inventory to a Pandas DataFrame
        return pd.DataFrame(self.inventory)

    def is_store_nearby(self, current_location, max_distance):
        # Calculate the distance from the current location to the store
        distance = np.linalg.norm(np.array(self.location) - np.array(current_location))
        return distance <= max_distance

    def meets_criteria(self, medicine_list, rating_threshold, current_location, max_distance):
        # Check if the store has all the medicines in the medicine_list
        has_medicines = all(
            any(med["Medicine"] == medicine for med in self.inventory)
            for medicine in medicine_list
        )

        # Check if the store meets the rating threshold
        meets_rating = self.rating >= rating_threshold

        # Check if the store is nearby
        nearby = self.is_store_nearby(current_location, max_distance)

        # Check if the store offers home delivery
        offers_delivery = self.home_delivery

        return has_medicines and meets_rating and nearby and offers_delivery


# Example medical stores
stores = [
    MedicalStore(
        name="HealthPlus Pharmacy",
        inventory=[
            {"Medicine": "Paracetamol", "Quantity": 50, "Price": 10.0},
            {"Medicine": "Aspirin", "Quantity": 30, "Price": 8.5},
        ],
        rating=4.5,
        location=[12.9716, 77.5946],
        home_delivery=True,
    ),
    MedicalStore(
        name="Wellness Drugstore",
        inventory=[
            {"Medicine": "Ibuprofen", "Quantity": 20, "Price": 15.0},
            {"Medicine": "Paracetamol", "Quantity": 40, "Price": 12.0},
        ],
        rating=4.0,
        location=[12.9650, 77.6050],
        home_delivery=False,
    ),
    MedicalStore(
        name="CareMed Pharmacy",
        inventory=[
            {"Medicine": "Paracetamol", "Quantity": 30, "Price": 10.0},
            {"Medicine": "Aspirin", "Quantity": 20, "Price": 8.5},
            {"Medicine": "Vitamin C", "Quantity": 50, "Price": 5.0},
        ],
        rating=4.8,
        location=[12.9800, 77.5900],
        home_delivery=True,
    ),
]

# Filter stores based on user requirements
current_location = [12.9716, 77.5946]  # User's current location
medicine_list = ["Paracetamol", "Aspirin"]  # Required medicines
rating_threshold = 4.0  # Minimum rating
max_distance = 5.0  # Maximum distance in km

nearby_stores = [
    store.name
    for store in stores
    if store.meets_criteria(medicine_list, rating_threshold, current_location, max_distance)
]

# Output the result
print("Medical stores near you with home delivery that meet your requirements:")
print(nearby_stores)
