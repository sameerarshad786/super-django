from geopy.geocoders import Nominatim


def get_countries(longitude, latitude):
    geolocator = Nominatim(user_agent="core")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    return location.raw.get("address")
