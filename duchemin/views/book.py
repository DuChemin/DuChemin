from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.book import DCBookSerializer
from duchemin.models.book import DCBook
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class BookListHTMLRenderer(CustomHTMLRenderer):
    template_name = "book/book_list.html"


class BookDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "book/book_detail.html"


class BookList(generics.ListAPIView):
    queryset = DCBook.objects.all()
    serializer_class = DCBookSerializer
    renderer_classes = (JSONRenderer, BookListHTMLRenderer)
    paginate_by = 100
    paginate_by_param = 'page_size'
    max_paginate_by = 200


class BookDetail(generics.RetrieveAPIView):
    queryset = DCBook.objects.all()
    lookup_field = "book_id"
    serializer_class = DCBookSerializer
    renderer_classes = (JSONRenderer, BookDetailHTMLRenderer)
