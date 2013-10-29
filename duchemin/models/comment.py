from django.db import models
from django.contrib.auth.models import User
from duchemin.models.piece import DCPiece

class DCComment(models.Model):

    piece = models.ForeignKey(DCPiece, related_name="comments")
    author = models.ForeignKey(User, related_name="comments")
    time = models.DateTimeField()
    text = models.TextField()

    def __unicode__(self):
        return u"{} ({} {})".format(self.piece,self.author,self.time)

    class Meta:
        app_label = "duchemin"
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
