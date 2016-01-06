from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.phrase import DCPhraseSerializer
from duchemin.models.phrase import DCPhrase
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class PhraseListHTMLRenderer(CustomHTMLRenderer):
    template_name = "phrase/phrase_list.html"


class PhraseDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "phrase/phrase_detail.html"


class PhraseList(generics.ListAPIView):
    queryset = DCPhrase.objects.all()
    serializer_class = DCPhraseSerializer
    renderer_classes = (JSONRenderer, PhraseListHTMLRenderer)
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 50


class PhraseDetail(generics.RetrieveAPIView):
    queryset = DCPhrase.objects.all()
    serializer_class = DCPhraseSerializer
    renderer_classes = (JSONRenderer, PhraseDetailHTMLRenderer)
