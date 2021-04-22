from django.db import models

# Create your models here.
class ad_settings(models.Model):
    creative_id = models.IntegerField()
    status = models.BooleanField(default=True)
    bidding_cpm = models.IntegerField()
    bid_quantity = models.IntegerField()
