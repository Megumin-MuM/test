from urllib.parse import urlparse, urlunparse
from django.shortcuts import render
from .crawler import get_chapter_title, search_books, get_book_details, get_chapter_content

def search(request):
    keyword = request.GET.get('q', '')
    books = search_books(keyword) if keyword else []
    return render(request, 'books/search_results.html', {'books': books, 'keyword': keyword})

def details(request, book_id):
    book_url = request.GET.get('url', '')
    chapters = get_book_details(book_url)
    return render(request, 'books/book_details.html', {'chapters': chapters})

def chapter(request, chapter_id):
    chapter_url = request.GET.get('url', '')

    parsed_url = urlparse(chapter_url)
    
    # 拆分路径并替换最后一个部分
    path_segments = parsed_url.path.split('/')
    path_segments[-1] = f"{chapter_id}.html"
    
    # 构建新的路径
    new_path = '/'.join(path_segments)
    
    # 构建新的 URL
    new_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        new_path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))
    
    content = get_chapter_content(new_url)
    title=get_chapter_title(new_url)
    return render(request, 'books/chapter_content.html', {'content': content, 'chapter_id': chapter_id, 'link': new_url,'title':title})
