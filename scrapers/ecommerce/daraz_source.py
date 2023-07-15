import os
import requests
import json

from urllib.request import urlopen
from decimal import Decimal

from django.db import transaction

from bs4 import BeautifulSoup
from psycopg2.extras import NumericRange

from supermarket.models import ProductSource, Products, ProductTypes


class Daraz(object):
    def __init__(self, domain) -> None:
        self.domain = domain

    def daraz_source(self):
        page = requests.get(self.domain)
        soup = BeautifulSoup(page.content, "html.parser")
        icon = soup.find("link", rel="icon")["href"]
        with transaction.atomic():
            try:
                product_source = ProductSource(
                    name="daraz",
                    icon=icon,
                    domain=self.domain
                )
                product_source.save()
            except:
                pass

        return product_source

    def daraz_products(self):
        page = urlopen("https://www.daraz.pk/smartphones/?spm=a2a0e.home.cate_7.1.35e34076OiMia3")
        soup = BeautifulSoup(page.read(), "html.parser")
        json_values = soup.select_one("script:-soup-contains('window.pageData')").text

        try:
            try_dump_data = json.loads(json_values.split("=", 1)[1])
        except json.JSONDecodeError:
            pass

        items = try_dump_data["mods"]["listItems"]
        for item in items:
            brand_name = item["brandName"] if not "No Brand" in item["brandName"].lower() else Products.Brand.NOT_DEFINED
            url = "https:" + item["productUrl"]
            price = float(item["price"])
            price_in_dollars = float(os.getenv("PKR_TO_DOLLAR_EXCHANGE_RATES")) * int(price)
            try:
                original_price = float(os.getenv("PKR_TO_DOLLAR_EXCHANGE_RATES")) * int(item["originalPrice"])
            except:
                original_price = price_in_dollars

            try:
                description = item["description"][0]
            except:
                description = ""

            product_source = ProductSource.objects.get(domain=self.domain)
            product_type = ProductTypes.objects.get(type="SMART PHONE")
            data = {
                "name": item["name"],
                "brand": brand_name if brand_name else Products.Brand.NOT_DEFINED,
                "url": url,
                "image": item["image"],
                "description": description,
                "ratings": Decimal(item["ratingScore"]) if item.get("ratingScore") else 0,
                "price": NumericRange(price_in_dollars),
                "original_price": original_price,
                "condition": Products.Condition.NOT_DEFINED,
                "shipping_charges": Decimal(item["shipping_charges"]) if item.get("shipping_charges") else 0,
                "product_source": product_source,
                "discount": int(item["discount"][:2]) if item.get("discount") else 0,
                "source": Products.Source.DARAZ,
                "type": product_type,
                "items_sold": 0
            }
            with transaction.atomic():
                try:
                    Products.objects.create(**data)
                except:
                    pass
