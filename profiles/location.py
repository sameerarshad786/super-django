import json

from urllib.request import urlopen


def get_location(request):
    ip = request.META.get("REMOTE_ADDR")
    url = f"https://www.ipinfo.io/{ip}/"
    with urlopen(url) as response:
        response_content = response.read()
    address = json.loads(response_content)
    return address
