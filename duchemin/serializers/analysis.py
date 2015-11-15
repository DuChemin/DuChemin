from duchemin.models.analysis import DCAnalysis
from duchemin.models.piece import DCPiece
from duchemin.models.phrase import DCPhrase
from duchemin.models.person import DCPerson
from rest_framework import serializers


class DCPersonAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPerson
        lookup_field = 'person_id'
        fields = ('url',)


class DCPieceAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    composer_id = DCPersonAnalysisSerializer()

    class Meta:
        model = DCPiece
        lookup_field = "piece_id"
        fields = ('url',
                  'composer_src',
                  'composer_id',
                  'title',
                  'book_position',
                  'pdf_link',
                  'mei_link',
                  'audio_link',
                  'forces',
                  'piece_id')


class DCPhraseAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCPhrase
        fields = ('url',)


class DCAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    composition_number = DCPieceAnalysisSerializer()
    phrase_number = DCPhraseAnalysisSerializer()
    analyst = DCPersonAnalysisSerializer()

    class Meta:
        model = DCAnalysis
        # fields = ('url',)
