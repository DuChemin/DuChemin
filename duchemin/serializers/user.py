from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    projects = serializers.HyperlinkedRelatedField(view_name='project-detail', many=True)
    workflows = serializers.HyperlinkedRelatedField(view_name="workflow-detail", many=True)
    workflow_runs = serializers.HyperlinkedRelatedField(view_name="workflowrun-detail", many=True)

    class Meta:
        model = User
        fields = ('url',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'is_staff',
                  'is_active',
                  'is_superuser',
                  'groups')


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', "last_name")
