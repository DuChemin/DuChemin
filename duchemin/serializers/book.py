from duchemin.models.book import DCBook
from duchemin.models.piece import DCPiece
from duchemin.models.person import DCPerson
from rest_framework import serializers


class DCBookPersonSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field('full_name')

    class Meta:
        model = DCPerson
        lookup_field = 'person_id'
        fields = ('url', 'full_name')


class DCBookPieceSerializer(serializers.HyperlinkedModelSerializer):
    composer_id = DCBookPersonSerializer()

    class Meta:
        model = DCPiece
        lookup_field = 'piece_id'
        fields = ('url', 'title', 'book_position', 'composer_id', 'composer_src', 'forces', 'print_concordances', 'ms_concordances')


class DCBookSerializer(serializers.HyperlinkedModelSerializer):
    pieces = DCBookPieceSerializer(many=True)

    class Meta:
        model = DCBook
        lookup_field = 'book_id'
        fields = ('url',
                  'title',
                  'complete_title',
                  'pieces',
                  'place_publication',
                  'date',
                  'volumes',
                  'part_st_id',
                  'part_cb_id',
                  'num_compositions',
                  'num_pages',
                  'location',
                  'rism',
                  'cesr',
                  'remarks',
                  'publisher')
