from duchemin.models.person import DCPerson
from duchemin.models.analysis import DCAnalysis
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase
from rest_framework import serializers


class DCPieceAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece
        lookup_field = 'piece_id'
        fields = ('url',)


class DCPhraseAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPhrase
        lookup_field = 'phrase_id'
        fields = ('url',)


class DCPersonAnalysesSerializer(serializers.HyperlinkedModelSerializer):
    # composition_number = DCPieceAnalysisSerializer(many=True)
    # phrase_number = DCPhraseAnalysisSerializer()

    class Meta:
        model = DCAnalysis
        fields = ('url',)


class DCPersonListSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field(source="full_name")

    class Meta:
        model = DCPerson
        lookup_field = 'person_id'
        fields = ('url',)


class DCPersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field(source="full_name")
    analyses = DCPersonAnalysesSerializer(many=True)

    class Meta:
        lookup_field = "person_id"
        model = DCPerson
        fields = ('url', 'full_name', 'analyses')