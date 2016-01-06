from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User

from duchemin.models.comment import DCComment
from duchemin.models.piece import DCPiece
from duchemin.serializers.comment import DCCommentSerializer
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


class CommentListHTMLRenderer(CustomHTMLRenderer):
    template_name = "discussion/discussion_list.html"


class PieceCommentDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "piece/piece_discussion.html"


class CommentList(generics.ListCreateAPIView):
    serializer_class = DCCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer, CommentListHTMLRenderer)
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 10

    def get_queryset(self):
        piece = self.request.QUERY_PARAMS.get('piece', None)
        last_update = self.request.QUERY_PARAMS.get('last_update', None)

        queryset = DCComment.objects.all()

        if last_update:
            queryset = queryset.filter(id__gt=last_update)

        if piece:
            queryset = queryset.filter(piece=piece)

        return queryset

    def post(self, request, *args, **kwargs):
        piece_id = request.DATA.get('piece_id', None)
        comment_text = request.DATA.get('comment_text', None)

        piece_obj = DCPiece.objects.get(piece_id=piece_id)
        current_user = User.objects.get(pk=request.user.id)

        comment = DCComment()
        comment.piece = piece_obj
        comment.author = current_user
        comment.text = comment_text
        comment.save()

        serialized = DCCommentSerializer(comment, context={'request': request}).data
        return Response(serialized, status=status.HTTP_201_CREATED)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DCComment.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DCCommentSerializer
    renderer_classes = (JSONRenderer,)
