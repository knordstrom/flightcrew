from datetime import datetime
from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field, field_validator, validator

from flightcrew.library.amadeus_sdk import SDK
from flightcrew.models.FlightsFound import FlightFinderToolInput, FlightsFound

class FlightFinderTool(BaseTool):
    """Flight Finder Tool"""
    sdk: SDK = None

    name: str = "Flight Finder Tool"
    description: str = (
        "This tool finds flights given the FlightFinderToolInput, including at a minimum the start date for travel and the origin airport code. "
    )
    args_schema: Type[BaseModel] = FlightFinderToolInput

    def __init__(self, sdk: SDK):
        super().__init__()
        self.sdk: SDK = sdk
        
    def _run(self, 
             start_date: datetime | str,
             origin: str,
             end_date: Optional[datetime | str] = None,
             destination: Optional[str] = None,
            #  max_price: Optional[float] = None,
            #  max_duration: Optional[int] = None,
             adults: Optional[int] = 2) -> FlightsFound:
        
        sd: str = start_date if isinstance(start_date, str) else datetime.astimezone().isoformat()

        params: dict[str, str] = {
            "departureDate": sd,
            "originLocationCode": origin,
            # "destinationLocationCode": destination,
            # "max_price": max_price,
            # "max_duration": max_duration
            "adults": f"{adults}"
        }
        if destination and destination != "" and destination != "None":
            params["destinationLocationCode"] = destination
        result: FlightsFound = self.sdk.find_flights(params=params)
        print("Found", len(result.results),"flights")
        return result
