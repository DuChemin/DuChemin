from django.db import models


class DCPhrase(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "Phrase"
        verbose_name_plural = "Phrases"
        ordering = ['piece_id', 'phrase_num']

    phrase_id = models.IntegerField(unique=True, db_index=True)
    piece_id = models.ForeignKey("duchemin.DCPiece", to_field='piece_id', related_name="phrases", db_index=True)
    phrase_num = models.IntegerField(blank=True, null=True)
    phrase_start = models.CharField(max_length=4, blank=True, null=True)
    phrase_stop = models.CharField(max_length=4, blank=True, null=True)
    phrase_text = models.CharField(max_length=255, blank=True, null=True)
    rhyme = models.CharField(max_length=64, blank=True, null=True)

    def __unicode__(self):
        return u"{0}.{1}: {2}".format(self.piece_id.piece_id, self.phrase_num, self.phrase_text)
