from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q


def search_product_using_es(index, name, page, size):
    client = Elasticsearch(
        hosts="https://localhost:9200",
        ca_certs=False,
        verify_certs=False,
        http_auth=("elastic", "0HKiYRk5XwrfL9F+*hts")
    )
    search_dict = {
        "query": {
            "match": {
                "name": "vivo"
            }
        }
    }


    # search = Search(using=client, index=index).from_dict(d=search_dict)

    # # Apply additional filters to the search
    # search = search.filter(Q("term", published=True))

    # # Execute the search
    # response = search.execute()


    es = Search(using=client, index=index)
    # query = Q("match", name='vivo')
    # es = es.query(query)
    es.from_dict(search_dict)

    response = es.execute()
    return response
