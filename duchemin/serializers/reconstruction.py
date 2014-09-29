from duchemin.models.reconstruction import DCReconstruction
from rest_framework import serializers


class DCReconstructionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DCReconstruction
