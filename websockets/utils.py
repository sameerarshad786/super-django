from django.core.paginator import Paginator
from channels.db import database_sync_to_async


async def paginate_response(count, page_number, serialized_function):
    paginator = Paginator(serialized_function, 10)
    page = await database_sync_to_async(paginator.get_page)(page_number)
    data = {
        'results': list(page),
        'count': count,
        'has_previous': page.has_previous(),
        'has_next': page.has_next(),
        'previous_page_number': page.previous_page_number() if page.has_previous() else None,
        'next_page_number': page.next_page_number() if page.has_next() else None,
    }
    return data
