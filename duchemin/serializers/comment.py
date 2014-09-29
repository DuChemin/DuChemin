from django.contrib.auth.models import User
from duchemin.models.comment import DCComment
from duchemin.models.piece import DCPiece
from duchemin.models.userprofile import DCUserProfile
from duchemin.models.person import DCPerson
from rest_framework import serializers


class DCPersonCommentSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field('full_name')

    class Meta:
        model = DCPerson
        lookup_field = "person_id"
        fields = ('url', 'person_id', 'full_name')


class DCUserProfileCommentSerializer(serializers.HyperlinkedModelSerializer):
    person = DCPersonCommentSerializer()

    class Meta:
        model = DCUserProfile
        fields = ('person',)


class DCUserCommentSerializer(serializers.HyperlinkedModelSerializer):
    profile = DCUserProfileCommentSerializer()

    class Meta:
        model = User
        fields = ('profile', 'username')


class DCPieceCommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        lookup_field = 'piece_id'
        fields = ('url', 'piece_id', 'title')


class DCCommentSerializer(serializers.HyperlinkedModelSerializer):
    author = DCUserCommentSerializer()
    piece = DCPieceCommentSerializer()

    class Meta:
        model = DCComment
        fields = ('id', 'author', 'piece', 'created', 'text',)
