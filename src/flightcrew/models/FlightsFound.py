from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class FlightTravelerSegmentAmenityProvider(BaseModel):
    """Traveler segment amenity provider schema."""
    name: str = Field(..., description="Name of the amenity provider.")
    # {
class FlightTravelerSegmentAmenity(BaseModel):
    """Traveler segment amenity schema."""
    description: str = Field(..., description="Description of the amenity.")
    isChargeable: bool = Field(..., description="Whether the amenity is chargeable.")
    amenityType: str = Field(..., description="Type of the amenity.")
    amenityProvider: FlightTravelerSegmentAmenityProvider = Field(..., description="Provider of the amenity.")

class FlightTravelerSegmentBags(BaseModel):
    """Traveler segment checked bags schema."""
    quantity: int = Field(..., description="Quantity of checked bags.")

class FlightTravelerSegmentPriceDetails(BaseModel):
    """Traveler segment price details schema."""
    segmentId: str = Field(..., description="Segment ID.")
    cabin: str = Field(..., description="Cabin class.")
    fareBasis: str = Field(..., description="Fare basis code.")
    brandedFare: str = Field(..., description="Branded fare code.")
    brandedFareLabel: str = Field(..., description="Branded fare label.")
    class_: str = Field(..., alias='class', description="Class of service.")
    includedCheckedBags: FlightTravelerSegmentBags = Field(..., description="Included checked bags details.")
    includedCabinBags: FlightTravelerSegmentBags = Field(..., description="Included cabin bags details.")
    amenities: list[FlightTravelerSegmentAmenity] = Field(..., description="List of amenities.")

class FlightTravelerPrice(BaseModel):
    """Traveler price schema."""
    currency: str = Field(..., description="Currency of the price.")
    total: str = Field(..., description="Total price.")
    base: str = Field(..., description="Base price.")

class FlightTravelerPricing(BaseModel):
    """Traveler pricing schema."""
    travelerId: str = Field(..., description="Traveler ID.")
    fareOption: str = Field(..., description="Fare option.")
    travelerType: str = Field(..., description="Traveler type.")
    price: FlightTravelerPrice = Field(..., description="Price details.")
    fareDetailsBySegment: list[FlightTravelerSegmentPriceDetails] = Field(..., description="Fare details by segment.")

class FlightPricingOptions(BaseModel):
    """Flight pricing options schema."""
    fareType: list[str] = Field(..., description="List of fare types.")
    includedCheckedBagsOnly: bool = Field(..., description="Whether only checked bags are included.")

class FlightPriceFee(BaseModel):
    """Flight price fee schema."""
    amount: str = Field(..., description="Amount of the fee.")
    type: str = Field(..., description="Type of the fee.")

    #{
class FlightPrice(BaseModel):
    """Flight price schema."""
    currency: str = Field(..., description="Currency of the price.")
    total: str = Field(..., description="Total price.")
    base: str = Field(..., description="Base price.")
    fees: list[FlightPriceFee] = Field(..., description="List of fees.")
    grandTotal: str = Field(..., description="Grand total price.")

class FlightSegment(BaseModel):
    """Flight segment schema."""
    departure: dict = Field(..., description="Departure details.")
    arrival: dict = Field(..., description="Arrival details.")
    carrierCode: str = Field(..., description="Carrier code.")
    number: str = Field(..., description="Flight number.")
    aircraft: dict = Field(..., description="Aircraft details.")
    duration: str = Field(..., description="Duration of the flight segment.")
    id: str = Field(..., description="ID of the flight segment.")
    numberOfStops: int = Field(..., description="Number of stops in the flight segment.")
    blacklistedInEU: bool = Field(..., description="Whether the flight is blacklisted in EU.")

class FlightItinerary(BaseModel):
    """Itinerary schema."""
    duration: str = Field(..., description="Duration of the itinerary.")
    segments: list[FlightSegment] = Field(..., description="List of segments in the itinerary.")
 
class FlightFound(BaseModel):
    type: str = Field(..., description="Type of the flight offer.")
    id: str = Field(..., description="ID of the flight offer.")
    source: str = Field(..., description="Source of the flight offer.")
    instantTicketingRequired: bool = Field(..., description="Whether instant ticketing is required.")
    nonHomogeneous: bool = Field(..., description="Whether the flight offer is non-homogeneous.")
    oneWay: bool = Field(..., description="Whether the flight offer is one-way.")
    isUpsellOffer: bool = Field(..., description="Whether the flight offer is an upsell offer.")
    lastTicketingDate: str = Field(..., description="Last ticketing date.")
    lastTicketingDateTime: str = Field(..., description="Last ticketing date and time.")
    numberOfBookableSeats: int = Field(..., description="Number of bookable seats.")
    itineraries: list[FlightItinerary] = Field(..., description="List of itineraries.")
    price: FlightPrice = Field(..., description="Price details.")
    pricingOptions: FlightPricingOptions = Field(..., description="Pricing options.")
    validatingAirlineCodes: list[str] = Field(..., description="List of validating airline codes.")
    travelerPricings: list[dict] = Field(..., description="List of traveler pricing details.")

class FlightsFound(BaseModel):
    results: list[FlightFound] = Field(..., description="List of flight offers found.")

    @staticmethod
    def from_response(response: list[dict[str, str]]) -> 'FlightsFound':
        """
        Create a FlightsFound instance from the API response.

        Args:
            response (dict): The API response.

        Returns:
            FlightsFound: An instance of FlightsFound.
        """
        results: list[FlightFound] = []
        for flight in response:
            # Convert the flight dictionary to a FlightFound instance
            flight_found = FlightFound(**flight)
            results.append(flight_found)
        return FlightsFound(results=results)
   
class FlightFinderToolInput(BaseModel):
    """Input schema for FlightFinderTool."""
    start_date: datetime | str = Field(..., description="Earliest date to look for flights.")
    end_date: Optional[datetime | str] = Field(default=None, description="Latest date to look for flights.")
    origin: str = Field(..., description="Origin airport code.")
    destination: Optional[str] = Field(..., description="Destination airport code.")
    # max_price: Optional[float] = Field(Optional[float], description="Maximum price for the flight.")
    # max_duration: Optional[int] = Field(Optional[int], description="Maximum duration of the flight in minutes.")
    adults: Optional[int] = Field(..., description="Number of adult passengers requested")

    # @field_validator('start_date', 'end_date', mode='before')
    # def validate_dates(cls, v: datetime) -> str:
    #     return v.isoformat()
