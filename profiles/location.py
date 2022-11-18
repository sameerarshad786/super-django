import json

from urllib.request import urlopen
from geopy.geocoders import Nominatim


def get_location(request):
    ip = request.META.get("REMOTE_ADDR")
    url = f"https://www.ipinfo.io/{ip}/"
    with urlopen(url) as response:
        response_content = response.read()
    address = json.loads(response_content)
    city = address.get("city")
    loc = Nominatim(user_agent="GetLoc")
    getLoc = loc.geocode(city)
    lang_loc = {"location": getLoc.address}
    return address, lang_loc
