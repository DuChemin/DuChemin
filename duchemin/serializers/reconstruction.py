from duchemin.models.reconstruction import DCReconstruction
from duchemin.models.piece import DCPiece
from duchemin.models.person import DCPerson
from rest_framework import serializers


class DCReconstructionPieceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        lookup_field = "piece_id"
        fields = ('url', 'title', 'piece_id')


class DCReconstructionPersonSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field(source="full_name")

    class Meta:
        model = DCPerson
        lookup_field = 'person_id'
        fields = ('url', 'full_name')

class DCReconstructionSerializer(serializers.HyperlinkedModelSerializer):
    piece = DCReconstructionPieceSerializer()
    reconstructor = DCReconstructionPersonSerializer()

    class Meta:
        model = DCReconstruction
        fields = ('url', 'piece', 'reconstructor')
