from django.db import models


class DCPerson(models.Model):
    class Meta:
        app_label = "duchemin"
        verbose_name = "Person"
        verbose_name_plural = "People"
        ordering = ['surname']

    person_id = models.CharField(max_length=16, unique=True, null=True, db_index=True)
    surname = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    given_name = models.CharField(max_length=64, blank=True, null=True)
    birth_date = models.CharField(max_length=16, blank=True, null=True)
    death_date = models.CharField(max_length=16, blank=True, null=True)
    active_date = models.CharField(max_length=16, blank=True, null=True)
    alt_spelling = models.CharField(max_length=64, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u"{0}, {1}".format(self.surname, self.given_name)

    @property
    def full_name(self):
        if self.given_name:
            return u"{0}, {1}".format(self.surname, self.given_name)
        else:
            return u"{0}".format(self.surname)

    @property
    def display_name(self):
        if self.given_name:
            return u"{0} {1}".format(self.given_name, self.surname)
        else:
            return u"{0}".format(self.surname)
