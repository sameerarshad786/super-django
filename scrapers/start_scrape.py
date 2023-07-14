from ecommerce.ebay_source import Ebay
from ecommerce.daraz_source import Daraz


if __name__ == "__main__":
    daraz_source = Daraz("https://www.daraz.pk/")
    ebay_source = Ebay("https://www.ebay.com/")

    ebay_source.ebay_source()
    daraz_source.daraz_source()

    daraz_source.daraz_products()
    ebay_source.ebay_products()
