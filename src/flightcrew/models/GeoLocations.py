from pydantic import BaseModel, Field


class GeoLocation(BaseModel):
    """
    A class to represent a geographical location with latitude and longitude.
    """
    name: str = Field(..., description="Full name of the location.")
    lat: float = Field(..., description="Latitude of the location.")
    lon: float = Field(..., description="Longitude of the location.")
    country: str = Field(..., description="Country of the location.")
    state: str = Field(..., description="State of the location.")

class GeoLocations(BaseModel):
    """
    A class to represent a list of geographical locations.
    """
    results: list[GeoLocation] 