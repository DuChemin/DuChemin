from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.piece import DCPieceSerializer
from duchemin.models.piece import DCPiece
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class PieceListHTMLRenderer(CustomHTMLRenderer):
    template_name = "piece/piece_list.html"


class PieceDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "piece/piece_detail.html"


class PieceDiscussionDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "piece/piece_discussion_detail.html"


class PieceList(generics.ListAPIView):
    model = DCPiece
    serializer_class = DCPieceSerializer
    renderer_classes = (JSONRenderer, PieceListHTMLRenderer)
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 20
    lookup_field = 'piece_id'


class PieceDetail(generics.RetrieveAPIView):
    model = DCPiece
    lookup_field = 'piece_id'
    serializer_class = DCPieceSerializer
    renderer_classes = (JSONRenderer, PieceDetailHTMLRenderer)


class PieceDiscussionDetail(generics.RetrieveAPIView):
    model = DCPiece
    lookup_field = 'piece_id'
    serializer_class = DCPieceSerializer
    renderer_classes = (JSONRenderer, PieceDiscussionDetailHTMLRenderer)
