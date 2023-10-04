from elasticsearch_dsl import Document, Text, Date
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch

from products.models import Products


class ProductIndex(Document):
    name = Text()
    brand = Date()
    description = Text()
    condition = Text()

    class Meta:
        index = 'product_index'


def bulk_indexing():    
    ProductIndex.init()    
    es = Elasticsearch()    
    bulk(client=es, actions=(b.indexing() for b in Products.objects.all().iterator()))
