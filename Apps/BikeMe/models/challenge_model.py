from django.db import models

class Challenge(models.Model):
    uid             = models.CharField(max_length=50, primary_key=True)
    typeChallenge   = models.IntegerField()
    condition       = models.IntegerField()
    award           = models.IntegerField()

    class Meta:
        ordering = ('typeChallenge','condition')