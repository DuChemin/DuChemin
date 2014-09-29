from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from duchemin.models.comment import DCComment
from duchemin.models.piece import DCPiece
from duchemin.serializers.comment import DCCommentSerializer
from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer


# Don't save comments that are essentially empty.
EMPTY_COMMENTS = ['Type a comment here', '', ' ']


# These will stick around, but if we're only using this for JSON serialization
# we won't need HTML templates.
# from duchemin.renderers.custom_html_renderer import CustomHTMLRenderer
class CommentListHTMLRenderer(CustomHTMLRenderer):
    template_name = "comment/comment_list.html"


class PieceCommentDetailHTMLRenderer(CustomHTMLRenderer):
    template_name = "piece/piece_discussion.html"


class CommentList(generics.ListCreateAPIView):
    model = DCComment
    serializer_class = DCCommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer, CommentListHTMLRenderer)
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 10

    def get_queryset(self):
        piece = self.request.QUERY_PARAMS.get('piece')
        last_update = self.request.QUERY_PARAMS.get('last_update', 0)
        queryset = DCComment.objects.filter(id__gt=last_update)

        if piece:
            queryset = queryset.filter(piece=piece)

        return queryset

    def post(self, request, *args, **kwargs):
        piece_id = request.DATA.get('piece_id', None)
        comment_text = request.DATA.get('text', None)

        piece_obj = get_object_or_404(DCPiece, piece_id=piece_id)

        if comment_text in EMPTY_COMMENTS:
            return Response({"message": "Empty Comments are not allowed."}, status=status.HTTP_400_BAD_REQUEST)

        current_user = User.objects.get(pk=request.user.id)
        comment = DCComment()
        comment.piece = piece_obj
        comment.author = current_user
        comment.text = comment_text
        comment.save()

        serialized = DCCommentSerializer(comment).data

        return Response(serialized, status=status.HTTP_201_CREATED)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    model = DCComment
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = DCCommentSerializer
    renderer_classes = (JSONRenderer,)
