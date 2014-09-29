from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from duchemin.models.piece import DCPiece
from django.core.signals import Signal
from django.db.models.signals import pre_save


class CommentViewTestCase(APITestCase):
    fixtures = ["1_users", "2_initial_data"]

    def setUp(self):
        pass

    def _create_comment(self):
        # helper method for creating comment
        pass

    def test_post(self):
        pass

    def test_get(self):
        pass

    def test_patch(self):
        pass

    def test_delete(self):
        pass

    def tearDown(self):
        pass
