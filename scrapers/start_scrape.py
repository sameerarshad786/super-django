from multiprocessing import Process

from ecommerce.ebay_source import Ebay
from ecommerce.daraz_source import Daraz


if __name__ == "__main__":
    daraz_source = Daraz("https://www.daraz.pk/")
    ebay_source = Ebay("https://www.ebay.com/")

    process1 = Process(target=daraz_source.daraz_products)
    process2 = Process(target=ebay_source.ebay_products)

    process1.start()
    process2.start()

    process1.join()
    process2.join()
