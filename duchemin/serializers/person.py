from duchemin.models.person import DCPerson
from duchemin.models.analysis import DCAnalysis
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase
from rest_framework import serializers


class DCPieceAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPiece


class DCPhraseAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPhrase


class DCPersonAnalysesSerializer(serializers.HyperlinkedModelSerializer):
    composition_number = DCPieceAnalysisSerializer()
    phrase_number = DCPhraseAnalysisSerializer()

    class Meta:
        model = DCAnalysis


class DCPersonListSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field(source="full_name")

    class Meta:
        model = DCPerson
        # fields = ('url',)


class DCPersonDetailSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field(source="full_name")
    analyses = DCPersonAnalysesSerializer()

    class Meta:
        lookup_field = "person_id"
        model = DCPerson