from rest_framework import views
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from duchemin.serializers.discussion import DCDiscussionSerializer
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class DiscussionListHTMLRenderer(CustomHTMLRenderer):
    template_name = "discussion/discussion_list.html"


class DiscussionList(views.APIView):
    serializer_class = DCDiscussionSerializer
    renderer_classes = (JSONRenderer, DiscussionListHTMLRenderer)
    paginate_by = 20
    paginate_by_param = 'page_size'
    max_paginate_by = 20
    lookup_field = 'piece_id'

    def get(self, request, format=None):
        return Response()
