from django.contrib.auth.models import User
from duchemin.models.piece import DCPiece
from duchemin.models.person import DCPerson
from duchemin.models.phrase import DCPhrase
from duchemin.models.book import DCBook
from duchemin.models.comment import DCComment
from duchemin.models.analysis import DCAnalysis
from duchemin.models.userprofile import DCUserProfile
from rest_framework import serializers


class DCBookPieceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DCBook
        lookup_field = 'book_id'
        fields = ('url', 'title')


class DCComposerPieceSerializer(serializers.HyperlinkedModelSerializer):
    full_name = serializers.Field('full_name')

    class Meta:
        model = DCPerson
        fields = ('url', 'full_name')
        lookup_field = 'person_id'


class DCPhrasePieceSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DCPhrase
        fields = ('url', 'phrase_text', 'phrase_num', 'phrase_start', 'phrase_stop', 'rhyme')


class DCAnalysisPieceSerializer(serializers.HyperlinkedModelSerializer):
    phrase_number = DCPhrasePieceSerializer()
    analyst = DCComposerPieceSerializer()

    class Meta:
        model = DCAnalysis
        fields = ('url',
                  'id',
                  'phrase_number',
                  'start_measure',
                  'stop_measure',
                  'analyst',
                  'is_cadence',
                  'cadence_kind',
                  'cadence_final_tone',
                  'cadence_role_cantz',
                  'cadence_role_tenz',
                  'cadence_alter',
                  'other_pres_type',
                  'voices_p6_up',
                  'voices_p6_lo',
                  'voices_p3_up',
                  'voices_p3_lo',
                  'voices_53_up',
                  'voices_53_lo',
                  'voice_role_up1_nim',
                  'voice_role_lo1_nim',
                  'voice_role_up2_nim',
                  'voice_role_lo2_nim',
                  'voice_role_dux1',
                  'voice_role_com1',
                  'voice_role_dux2',
                  'voice_role_com2',
                  'voice_role_un_oct',
                  'voice_role_fifth',
                  'voice_role_fourth',
                  'voice_role_above',
                  'voice_role_below',
                  'other_formulas',
                  'other_contrapuntal',
                  'text_treatment',
                  'repeat_kind',
                  'earlier_phrase',
                  'repeat_exact_varied',
                  'comment',
                  'nanopub_link')


class DCUserCommentSerializer(serializers.HyperlinkedModelSerializer):
    profile = serializers.SerializerMethodField('get_user_profile_url')
    display_name = serializers.SerializerMethodField('get_profile_display_name')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'profile', 'display_name')

    def get_user_profile_url(self, obj):
        request = self.context.get('request', None)
        if not request.user.is_authenticated():
            return ""
        url = request.build_absolute_uri("/person/{0}".format(obj.profile.person.person_id))
        return url

    def get_profile_display_name(self, obj):
        return obj.profile.person.display_name


class DCPieceCommentSerializer(serializers.HyperlinkedModelSerializer):
    author = DCUserCommentSerializer()

    class Meta:
        model = DCComment
        fields = ('url', 'text', 'author', 'created')


class DCPieceSerializer(serializers.HyperlinkedModelSerializer):
    composer_id = DCComposerPieceSerializer()
    phrases = DCPhrasePieceSerializer()
    book_id = DCBookPieceSerializer()
    analyses = DCAnalysisPieceSerializer()
    comments = DCPieceCommentSerializer(many=True)

    class Meta:
        model = DCPiece
        lookup_field = "piece_id"
        fields = ('url',
                  'piece_id',
                  'title',
                  'composer_id',
                  'phrases',
                  'mei_link',
                  'pdf_link',
                  'audio_link',
                  'book_id',
                  'analyses',
                  'comments')