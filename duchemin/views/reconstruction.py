from rest_framework import generics
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.reconstruction import DCReconstructionSerializer
from duchemin.models.reconstruction import DCReconstruction
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class ReconstructionListHTMLRenderer(CustomHTMLRenderer):
    template_name = "reconstruction/reconstruction_list.html"


class ReconstructionDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "reconstruction/reconstruction_detail.html"


class ReconstructionList(generics.ListAPIView):
    model = DCReconstruction
    serializer_class = DCReconstructionSerializer
    renderer_classes = (JSONRenderer, ReconstructionListHTMLRenderer)
    paginate_by = 50
    paginate_by_param = 'page_size'
    max_paginate_by = 50


class ReconstructionDetail(generics.RetrieveAPIView):
    model = DCReconstruction
    lookup_field = 'piece_id'
    serializer_class = DCReconstructionSerializer
    renderer_classes = (JSONRenderer, ReconstructionDetailHTMLRenderer)
