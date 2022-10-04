from django.core.paginator import Paginator

from helper import keys


def apply_pagination(request, queryset):
    page_count = int(request.GET.get(keys.PAGE_COUNT, 10))
    paginator = Paginator(queryset, page_count)
    page_total = int(paginator.num_pages)
    total_count = int(paginator.count)
    page_number = int(request.GET.get(keys.PAGE_NUMBER, 1))
    new_queryset = paginator.get_page(page_number).object_list
    return new_queryset, dict(
        page_total=page_total,
        page_number=page_number,
        page_count=page_count,
        total_count=total_count
    )
