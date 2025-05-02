import os
import requests
from amadeus import Client


class SDK:
    """
    The SDK class is a placeholder for the FlightCrew SDK.
    It currently does not contain any methods or attributes.
    """

    def __init__(self):
        self.api_key: str = os.getenv('AMADEUS_API_KEY')
        self.api_secret: str = os.getenv('AMADEUS_API_SECRET')
        self.base_domain: str = os.getenv('AMADEUS_BASE_DOMAIN')
        self.amadeus: Client = None
        
    def authenticate(self) -> None:
        """
        Authenticate against the amadeus API and return the token.
        """
        self.amadeus: Client = Client(
            client_id=self.api_key,
            client_secret=self.api_secret,
        )

    def find_flights(self, params: dict) -> dict:
        """
        Search for flights using the Amadeus API with known destinations and dates.
        """
        try:
            print("Finding flights with params:", params)
            response = self.amadeus.shopping.flight_offers_search.get(**params)
            if response.status_code == 200:
                print("Flights found successfully.")
                return response.data
            else:
                print(f"Response was {response.status_code} - {response.reason}")
                raise Exception(f"Error: {response.status_code} - {response.reason}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {e}")
        
        

    