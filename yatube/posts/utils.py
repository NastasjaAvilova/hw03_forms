from django.core.paginator import Paginator


def get_page_context(posts, request, last_posts):
    paginator = Paginator(posts, last_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
