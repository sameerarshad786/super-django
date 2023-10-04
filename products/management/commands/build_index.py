from django.core.management.base import BaseCommand

from elasticsearch import Elasticsearch


class Command(BaseCommand):
    help = 'Release spider'

    def handle(self, *args, **options):
        client = Elasticsearch(
            hosts="https://localhost:9200",
            ca_certs=False,
            verify_certs=False,
            http_auth=("elastic", "0HKiYRk5XwrfL9F+*hts")
        )
        index_settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            },
            "mappings": {
                "properties": {
                    "name": {"type": "text"},
                    "description": {"type": "text"}
                }
            }
        }

        index_name = "product_index"  # Replace with your desired index name
        response = client.indices.create(index=index_name, body=index_settings, ignore=400)
        print(response)
