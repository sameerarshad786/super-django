import os
import requests
import json

from io import BytesIO
from urllib.request import urlopen
from decimal import Decimal

from django.db import transaction
from django.core.files import File

from bs4 import BeautifulSoup
from psycopg2.extras import NumericRange
from PIL import Image

from supermarket.models import ProductSource, Products, ProductTypes


class Daraz(object):
    def __init__(self, domain) -> None:
        self.domain = domain

    def daraz_source(self):
        page = requests.get(self.domain)
        soup = BeautifulSoup(page.content, "html.parser")
        icon_link = soup.find("link", rel="icon")["href"]
        get_icon_link = urlopen(f"https:{icon_link}")
        file = BytesIO(get_icon_link.read())
        icon = File(file, name="daraz-icon.png")
        with transaction.atomic():
            try:
                product_source = ProductSource.objects.get(domain=self.domain)
            except ProductSource.DoesNotExist:
                product_source = ProductSource(
                    name="daraz",
                    icon=icon,
                    domain=self.domain
                )
                product_source.save()

        return product_source

    def daraz_products(self):
        page = urlopen("https://www.daraz.pk/smartphones/?spm=a2a0e.home.cate_7.1.35e34076OiMia3")
        soup = BeautifulSoup(page.read(), "html.parser")
        scripts = soup.find_all("script")
        result = [index for index, script in enumerate(scripts) if script.text.startswith("window.pageData")]
        json_values = soup.find_all("script")[result[0]].text

        for json_value in json_values.split("=", 1):
            try:
                if try_dump_data := json.loads(json_value):
                    items = try_dump_data["mods"]["listItems"]
                    for item in items:
                        brand_name = item["brandName"] if not "No Brand" in item["brandName"].lower() else ""
                        url = "https:" + item["productUrl"]
                        price = item["price"]
                        price_in_dollars = round(
                            os.getenv("PKR_TO_DOLLAR_EXCHANGE_RATES") * float(price),
                            2
                        )
                        try:
                            ratings = item["ratingScore"]
                        except:
                            ratings = 0
                        
                        try:
                            original_price = round(
                                os.getenv("PKR_TO_DOLLAR_EXCHANGE_RATES") * float(item["originalPrice"]),
                                2
                            )
                        except:
                            original_price = price_in_dollars
                        
                        try:
                            discount = int(item["discount"][:2])
                        except:
                            discount = 0
                        
                        try:
                            description = item["description"][0]
                        except:
                            description = ""
                        
                        try:
                            shipping_charges = item["shipping_charges"]
                        except:
                            shipping_charges = 0

                        image_url = item["image"]
                        image_url = requests.get(image_url)
                        image = BytesIO(image_url.content)
                        name = item["name"]
                        file = File(image, name=f"{name[:40].strip()}.png")
                        if file.size > 1000000:
                            file = Image.open(file)
                            file.save(f"{name[:40].strip()}.png", quality=90, optimize=True)
                        product_source = self.daraz_source()
                        try:
                            product_type = ProductTypes.objects.get(type="SMART PHONE", valid_name=True)
                        except ProductTypes.DoesNotExist:
                            product_type = ProductTypes.objects.create(type="SMART PHONE", valid_name=True)
                        data = {
                            "name": name,
                            "brand": brand_name,
                            "url": url,
                            "image": file,
                            "description": description,
                            "ratings": Decimal(ratings),
                            "price": NumericRange(price_in_dollars),
                            "original_price": original_price,
                            "condition": Products.Condition.NOT_DEFINED,
                            "brand": Products.Brand.NOT_DEFINED,
                            "shipping_charges": Decimal(shipping_charges),
                            "product_source": product_source,
                            "discount": discount,
                            "source": Products.Source.DARAZ,
                            "type": product_type,
                            "items_sold": 0
                        }
                        with transaction.atomic():
                            try:
                                scraped_product = Products(**data)
                                scraped_product.save()

                            except Exception as e:
                                print(e)

            except Exception as e:
                continue
