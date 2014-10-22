from django.db import models
from django.contrib.auth.models import User


class DCUserProfile(models.Model):
    class Meta:
        app_label = "duchemin"

    user = models.OneToOneField(User, db_index=True)
    favourited_piece = models.ManyToManyField("duchemin.DCPiece", blank=True, db_index=True)
    favourited_analysis = models.ManyToManyField("duchemin.DCAnalysis", blank=True, db_index=True)
    favourited_reconstruction = models.ManyToManyField("duchemin.DCReconstruction", blank=True, db_index=True)
    role = models.CharField(max_length=64, blank=True, null=True)
    person = models.ForeignKey("duchemin.DCPerson", blank=True, null=True, help_text="Link this account with a DuChemin User", db_index=True, related_name="profile")

    def __unicode__(self):
        return u"{0}, {1}".format(self.user.last_name, self.user.first_name)

User.profile = property(lambda u: DCUserProfile.objects.get_or_create(user=u)[0])