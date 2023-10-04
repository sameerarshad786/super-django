from django.core.management.base import BaseCommand

from elasticsearch import Elasticsearch

from products.models import Products


class Command(BaseCommand):
    help = 'Rinsert data'

    def handle(self, *args, **options):
        client = Elasticsearch(
            hosts="https://localhost:9200",
            ca_certs=False,
            verify_certs=False,
            http_auth=("elastic", "0HKiYRk5XwrfL9F+*hts")
        )
        total = Products.objects.all().count()
        for product, id in zip(Products.objects.all(), range(3, total)):
            document = {
                "id": str(product.id),
                "name": product.name,
                "brand": product.brand,
                "type": product.type.type,
                "image": product.image,
                "url": product.url,
                "items_sold": product.items_sold,
                "rating": product.ratings,
                "condition": product.condition,
                "original_price": product.original_price,
                "shipping_charges": product.shipping_charges,
                "source": product.source,
                "discount": product.discount
            }
            response = client.create(
                index="product_index",
                id=id,
                document=document
            )
            print(response)
