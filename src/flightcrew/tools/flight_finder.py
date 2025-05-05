from datetime import datetime
from crewai.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field, field_validator, validator

from flightcrew.library.sdk import SDK

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
   
class FlightFinderToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    start_date: datetime | str = Field(..., description="Earliest date to look for flights.")
    end_date: Optional[datetime] | Optional[str] = Field(..., description="Latest date to look for flights.")
    origin: str = Field(..., description="Origin airport code.")
    destination: Optional[str] = Field(..., description="Destination airport code.")
    # max_price: Optional[float] = Field(Optional[float], description="Maximum price for the flight.")
    # max_duration: Optional[int] = Field(Optional[int], description="Maximum duration of the flight in minutes.")
    adults: Optional[int] = Field(..., description="Number of adult passengers requested")

    # @field_validator('start_date', 'end_date', mode='before')
    # def validate_dates(cls, v: datetime) -> str:
    #     return v.isoformat()

class FlightFinderTool(BaseTool):
    """Flight Finder Tool."""
    sdk: SDK = None

    name: str = "Flight Finder Tool"
    description: str = (
        "This tool finds flights given the FlightFinderToolInput."
    )
    args_schema: Type[BaseModel] = FlightFinderToolInput

    def __init__(self, sdk: SDK):
        super().__init__()
        self.sdk: SDK = sdk
        
    def _run(self, 
             start_date: datetime | str,
             end_date: datetime | str,
             origin: str,
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
        result: list[dict[str,str]] = self.sdk.find_flights(params=params)
        output: list[FlightFound] = []
        for flight in result:
            ff = FlightFound(**flight)
            output.append(ff)
        final_output = FlightsFound(results=output)
        print("Found", len(output),"flights")
        return final_output

# [
#   {
#     "type": "flight-offer",
#     "id": "1",
#     "source": "GDS",
#     "instantTicketingRequired": false,
#     "nonHomogeneous": false,
#     "oneWay": false,
#     "isUpsellOffer": false,
#     "lastTicketingDate": "2025-05-02",
#     "lastTicketingDateTime": "2025-05-02",
#     "numberOfBookableSeats": 9,
#     "itineraries": [
#       {
#         "duration": "PT1H17M",
#         "segments": [
#           {
#             "departure": {
#               "iataCode": "DEN",
#               "at": "2025-06-02T08:15:00"
#             },
#             "arrival": {
#               "iataCode": "SAF",
#               "at": "2025-06-02T09:32:00"
#             },
#             "carrierCode": "UA",
#             "number": "5822",
#             "aircraft": {
#               "code": "CR7"
#             },
#             "duration": "PT1H17M",
#             "id": "1",
#             "numberOfStops": 0,
#             "blacklistedInEU": false
#           }
#         ]
#       }
#     ],
#     "price": {
#       "currency": "EUR",
#       "total": "188.70",
#       "base": "163.00",
#       "fees": [
#         {
#           "amount": "0.00",
#           "type": "SUPPLIER"
#         },
#         {
#           "amount": "0.00",
#           "type": "TICKETING"
#         }
#       ],
#       "grandTotal": "188.70"
#     },
#     "pricingOptions": {
#       "fareType": [
#         "PUBLISHED"
#       ],
#       "includedCheckedBagsOnly": false
#     },
#     "validatingAirlineCodes": [
#       "UA"
#     ],
#     "travelerPricings": [
#       {
#         "travelerId": "1",
#         "fareOption": "STANDARD",
#         "travelerType": "ADULT",
#         "price": {
#           "currency": "EUR",
#           "total": "188.70",
#           "base": "163.00"
#         },
#         "fareDetailsBySegment": [
#           {
#             "segmentId": "1",
#             "cabin": "ECONOMY",
#             "fareBasis": "VAA2ADEN",
#             "brandedFare": "ECONOMY",
#             "brandedFareLabel": "ECONOMY",
#             "class": "V",
#             "includedCheckedBags": {
#               "quantity": 0
#             },
#             "includedCabinBags": {
#               "quantity": 1
#             },
#             "amenities": [
#               {
#                 "description": "CHECKED BAG FIRST",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "SECOND BAG",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRE RESERVED SEAT ASSIGNMENT",
#                 "isChargeable": false,
#                 "amenityType": "PRE_RESERVED_SEAT",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRIORITY BOARDING",
#                 "isChargeable": true,
#                 "amenityType": "TRAVEL_SERVICES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "ECONOMY TO ECONOMY PLUS",
#                 "isChargeable": true,
#                 "amenityType": "UPGRADES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "MILEAGE ACCRUAL",
#                 "isChargeable": false,
#                 "amenityType": "BRANDED_FARES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   },
#   {
#     "type": "flight-offer",
#     "id": "2",
#     "source": "GDS",
#     "instantTicketingRequired": false,
#     "nonHomogeneous": false,
#     "oneWay": false,
#     "isUpsellOffer": false,
#     "lastTicketingDate": "2025-05-02",
#     "lastTicketingDateTime": "2025-05-02",
#     "numberOfBookableSeats": 9,
#     "itineraries": [
#       {
#         "duration": "PT1H21M",
#         "segments": [
#           {
#             "departure": {
#               "iataCode": "DEN",
#               "at": "2025-06-02T20:33:00"
#             },
#             "arrival": {
#               "iataCode": "SAF",
#               "at": "2025-06-02T21:54:00"
#             },
#             "carrierCode": "UA",
#             "number": "4684",
#             "aircraft": {
#               "code": "CR7"
#             },
#             "duration": "PT1H21M",
#             "id": "3",
#             "numberOfStops": 0,
#             "blacklistedInEU": false
#           }
#         ]
#       }
#     ],
#     "price": {
#       "currency": "EUR",
#       "total": "188.70",
#       "base": "163.00",
#       "fees": [
#         {
#           "amount": "0.00",
#           "type": "SUPPLIER"
#         },
#         {
#           "amount": "0.00",
#           "type": "TICKETING"
#         }
#       ],
#       "grandTotal": "188.70"
#     },
#     "pricingOptions": {
#       "fareType": [
#         "PUBLISHED"
#       ],
#       "includedCheckedBagsOnly": false
#     },
#     "validatingAirlineCodes": [
#       "UA"
#     ],
#     "travelerPricings": [
#       {
#         "travelerId": "1",
#         "fareOption": "STANDARD",
#         "travelerType": "ADULT",
#         "price": {
#           "currency": "EUR",
#           "total": "188.70",
#           "base": "163.00"
#         },
#         "fareDetailsBySegment": [
#           {
#             "segmentId": "3",
#             "cabin": "ECONOMY",
#             "fareBasis": "VAA2ADEN",
#             "brandedFare": "ECONOMY",
#             "brandedFareLabel": "ECONOMY",
#             "class": "V",
#             "includedCheckedBags": {
#               "quantity": 0
#             },
#             "includedCabinBags": {
#               "quantity": 1
#             },
#             "amenities": [
#               {
#                 "description": "CHECKED BAG FIRST",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "SECOND BAG",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRE RESERVED SEAT ASSIGNMENT",
#                 "isChargeable": false,
#                 "amenityType": "PRE_RESERVED_SEAT",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRIORITY BOARDING",
#                 "isChargeable": true,
#                 "amenityType": "TRAVEL_SERVICES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "ECONOMY TO ECONOMY PLUS",
#                 "isChargeable": true,
#                 "amenityType": "UPGRADES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "MILEAGE ACCRUAL",
#                 "isChargeable": false,
#                 "amenityType": "BRANDED_FARES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   },
#   {
#     "type": "flight-offer",
#     "id": "3",
#     "source": "GDS",
#     "instantTicketingRequired": false,
#     "nonHomogeneous": false,
#     "oneWay": false,
#     "isUpsellOffer": false,
#     "lastTicketingDate": "2025-05-02",
#     "lastTicketingDateTime": "2025-05-02",
#     "numberOfBookableSeats": 9,
#     "itineraries": [
#       {
#         "duration": "PT1H26M",
#         "segments": [
#           {
#             "departure": {
#               "iataCode": "DEN",
#               "at": "2025-06-02T16:00:00"
#             },
#             "arrival": {
#               "iataCode": "SAF",
#               "at": "2025-06-02T17:26:00"
#             },
#             "carrierCode": "UA",
#             "number": "5643",
#             "aircraft": {
#               "code": "CR7"
#             },
#             "duration": "PT1H26M",
#             "id": "4",
#             "numberOfStops": 0,
#             "blacklistedInEU": false
#           }
#         ]
#       }
#     ],
#     "price": {
#       "currency": "EUR",
#       "total": "188.70",
#       "base": "163.00",
#       "fees": [
#         {
#           "amount": "0.00",
#           "type": "SUPPLIER"
#         },
#         {
#           "amount": "0.00",
#           "type": "TICKETING"
#         }
#       ],
#       "grandTotal": "188.70"
#     },
#     "pricingOptions": {
#       "fareType": [
#         "PUBLISHED"
#       ],
#       "includedCheckedBagsOnly": false
#     },
#     "validatingAirlineCodes": [
#       "UA"
#     ],
#     "travelerPricings": [
#       {
#         "travelerId": "1",
#         "fareOption": "STANDARD",
#         "travelerType": "ADULT",
#         "price": {
#           "currency": "EUR",
#           "total": "188.70",
#           "base": "163.00"
#         },
#         "fareDetailsBySegment": [
#           {
#             "segmentId": "4",
#             "cabin": "ECONOMY",
#             "fareBasis": "VAA2ADEN",
#             "brandedFare": "ECONOMY",
#             "brandedFareLabel": "ECONOMY",
#             "class": "V",
#             "includedCheckedBags": {
#               "quantity": 0
#             },
#             "includedCabinBags": {
#               "quantity": 1
#             },
#             "amenities": [
#               {
#                 "description": "CHECKED BAG FIRST",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "SECOND BAG",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRE RESERVED SEAT ASSIGNMENT",
#                 "isChargeable": false,
#                 "amenityType": "PRE_RESERVED_SEAT",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRIORITY BOARDING",
#                 "isChargeable": true,
#                 "amenityType": "TRAVEL_SERVICES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "ECONOMY TO ECONOMY PLUS",
#                 "isChargeable": true,
#                 "amenityType": "UPGRADES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "MILEAGE ACCRUAL",
#                 "isChargeable": false,
#                 "amenityType": "BRANDED_FARES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   },
#   {
#     "type": "flight-offer",
#     "id": "4",
#     "source": "GDS",
#     "instantTicketingRequired": false,
#     "nonHomogeneous": false,
#     "oneWay": false,
#     "isUpsellOffer": false,
#     "lastTicketingDate": "2025-05-02",
#     "lastTicketingDateTime": "2025-05-02",
#     "numberOfBookableSeats": 9,
#     "itineraries": [
#       {
#         "duration": "PT1H19M",
#         "segments": [
#           {
#             "departure": {
#               "iataCode": "DEN",
#               "at": "2025-06-02T11:21:00"
#             },
#             "arrival": {
#               "iataCode": "SAF",
#               "at": "2025-06-02T12:40:00"
#             },
#             "carrierCode": "UA",
#             "number": "5310",
#             "aircraft": {
#               "code": "CR7"
#             },
#             "duration": "PT1H19M",
#             "id": "2",
#             "numberOfStops": 0,
#             "blacklistedInEU": false
#           }
#         ]
#       }
#     ],
#     "price": {
#       "currency": "EUR",
#       "total": "315.55",
#       "base": "281.00",
#       "fees": [
#         {
#           "amount": "0.00",
#           "type": "SUPPLIER"
#         },
#         {
#           "amount": "0.00",
#           "type": "TICKETING"
#         }
#       ],
#       "grandTotal": "315.55"
#     },
#     "pricingOptions": {
#       "fareType": [
#         "PUBLISHED"
#       ],
#       "includedCheckedBagsOnly": false
#     },
#     "validatingAirlineCodes": [
#       "UA"
#     ],
#     "travelerPricings": [
#       {
#         "travelerId": "1",
#         "fareOption": "STANDARD",
#         "travelerType": "ADULT",
#         "price": {
#           "currency": "EUR",
#           "total": "315.55",
#           "base": "281.00"
#         },
#         "fareDetailsBySegment": [
#           {
#             "segmentId": "2",
#             "cabin": "ECONOMY",
#             "fareBasis": "UAA4ODEN",
#             "brandedFare": "ECONOMY",
#             "brandedFareLabel": "ECONOMY",
#             "class": "U",
#             "includedCheckedBags": {
#               "quantity": 0
#             },
#             "includedCabinBags": {
#               "quantity": 1
#             },
#             "amenities": [
#               {
#                 "description": "CHECKED BAG FIRST",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "SECOND BAG",
#                 "isChargeable": true,
#                 "amenityType": "BAGGAGE",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRE RESERVED SEAT ASSIGNMENT",
#                 "isChargeable": false,
#                 "amenityType": "PRE_RESERVED_SEAT",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "PRIORITY BOARDING",
#                 "isChargeable": true,
#                 "amenityType": "TRAVEL_SERVICES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "ECONOMY TO ECONOMY PLUS",
#                 "isChargeable": true,
#                 "amenityType": "UPGRADES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               },
#               {
#                 "description": "MILEAGE ACCRUAL",
#                 "isChargeable": false,
#                 "amenityType": "BRANDED_FARES",
#                 "amenityProvider": {
#                   "name": "BrandedFare"
#                 }
#               }
#             ]
#           }
#         ]
#       }
#     ]
#   }
# ]