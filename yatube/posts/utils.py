from django.core.paginator import Paginator


def get_page_context(request, posts, last_posts):
    paginator = Paginator(posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj
