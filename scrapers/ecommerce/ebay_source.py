import requests

from io import BytesIO
from urllib.request import urlopen
from decimal import Decimal

from django.db import transaction
from django.core.files import File

from bs4 import BeautifulSoup
from psycopg2.extras import NumericRange
from PIL import Image

from supermarket.models import ProductSource, Products, ProductTypes


class Ebay(object):
    def __init__(self, domain) -> None:
        self.domain = domain

    def ebay_source(self):
        page = requests.get(self.domain)
        soup = BeautifulSoup(page.content, "html.parser")
        icon_link = soup.find("link", rel="icon")["href"]
        get_icon_link = requests.get(icon_link)
        file = BytesIO(get_icon_link.content)
        icon = File(file, name="ebay-icon.png")
        with transaction.atomic():
            try:
                product_source = ProductSource.objects.get(domain=self.domain)
            except:
                product_source = ProductSource(
                    name="ebay",
                    icon=icon,
                    domain=self.domain
                )
                product_source.save()

            return product_source

    def ebay_products(self):
        page = urlopen("https://www.ebay.com/b/Cell-Phones-Smart-Watches-Accessories/15032/bn_1865441")
        soup = BeautifulSoup(page.read(), "html.parser")
        brand_div = soup.find_all("div", class_="b-visualnav__grid")
        brands = brand_div[1].find_all("a", class_="b-visualnav__tile b-visualnav__tile__default")
        for brand in brands:
            brand_name = brand.find("div", class_="b-visualnav__title").text.split(" ")[0].lower()
            brands_page = urlopen(brand["href"])
            soup = BeautifulSoup(brands_page.read(), "html.parser")
            for product in soup.find_all("div", "s-item__wrapper clearfix"):
                name = product.find("h3", "s-item__title").text
                price = product.find("span", class_="s-item__price").text

                try:
                    shipping_charges = Decimal(product.find("span", class_="s-item__shipping s-item__logisticsCost").text.split(" ")[0][1:])
                except:
                    shipping_charges = 0

                try:
                    items_sold = product.find("span", class_="NEGATIVE")
                    if items_sold.text:
                        if "only" in items_sold.text.lower():
                            items_sold = items_sold.text.split(" ")[1]
                        elif "watching" in items_sold.text.lower():
                            items_sold = 0
                        else:
                            items_sold = items_sold.text.split(" ")[0].replace(",", "")
                except:
                    items_sold = 0

                try:
                    condition = product.find("span", class_="s-item__certified-refurbished s-item__certified-refurbished--isLarge").text
                except:
                    condition = None

                try:
                    ratings = product.find("div", class_="star-rating b-rating__rating-star")["aria-label"].split(" ")[0]
                except:
                    ratings = 0

                url = product.find("a", "s-item__link")["href"]
                try:
                    image_url = product.find("img", "s-item__image-img")["data-src"]
                except:
                    image_url = product.find("img", "s-item__image-img")["src"]
                image_url = requests.get(image_url)
                image = BytesIO(image_url.content)
                file = File(image, name=f"{name[:40].strip()}.png")
                if file.size > 1000000:
                    file = Image.open(file)
                    file.save(f"{name[:40].strip()}.png", quality=90, optimize=True)
                product_source = self.ebay_source()
                try:
                    product_type = ProductTypes.objects.get(type="SMART PHONE", valid_name=True)
                except ProductTypes.DoesNotExist:
                    product_type = ProductTypes.objects.create(type="SMART PHONE", valid_name=True)

                _price = 0.00
                min_value = 0
                if "to" in price:
                    price_range = price.split(" to ")
                    min_value = price_range[0][1:].replace(",", "")
                    max_value = price_range[1][1:].replace(",", "")
                    _price = NumericRange(Decimal(min_value), Decimal(max_value))
                else:
                    single_value = price[1:]
                    min_value = single_value
                    _price = NumericRange(Decimal(single_value))

                try:
                    original_price = Decimal(product.find("span", class_="STRIKETHROUGH").text[1:])
                except:
                    original_price = Decimal(min_value)

                discount = ((original_price-Decimal(min_value))/Decimal(original_price))*100 if original_price!= min_value else 0

                data = {
                    "name": name,
                    "brand": brand_name if brand_name else Products.Brand.NOT_DEFINED,
                    "url": url,
                    "image": file,
                    "ratings": Decimal(ratings),
                    "price": _price,
                    "original_price": original_price,
                    "discount": discount,
                    "condition": condition.split(" ")[1].lower() if condition else Products.Condition.USED,
                    "shipping_charges": shipping_charges,
                    "product_source": product_source,
                    "source": Products.Source.EBAY,
                    "type": product_type,
                    "items_sold": items_sold
                }
                with transaction.atomic():
                    try:
                        scraped_product = Products(**data)
                        scraped_product.save()

                    except Exception as e:
                        print(e)
