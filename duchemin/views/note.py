from rest_framework import generics, permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.http import Http404

from duchemin.models.note import DCNote
from duchemin.models.piece import DCPiece
from duchemin.serializers.note import DCNoteSerializer


class NoteList(generics.ListCreateAPIView):
    serializer_class = DCNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        current_user = self.request.user
        return DCNote.objects.filter(author=current_user)

    def post(self, request, *args, **kwargs):
        piece_id = request.data.get('piece_id', None)
        note_text = request.data.get('text', None)

        piece_obj = get_object_or_404(DCPiece, piece_id=piece_id)
        current_user = request.user

        note = DCNote(piece=piece_obj, author=current_user, text=note_text)
        note.save()

        serialized = DCNoteSerializer(note).data
        return Response(serialized, status=status.HTTP_201_CREATED)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DCNoteSerializer
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (JSONRenderer,)

    def get_object(self):
        current_user = self.request.user
        note = DCNote.objects.filter(author=current_user, piece__piece_id=self.kwargs["pk"]).order_by("-updated").first()
        if not note:
            raise Http404
        return note

    def get_queryset(self):
        current_user = self.request.user
        return DCNote.objects.filter(author=current_user)