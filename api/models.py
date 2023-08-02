from django.db import models

# Create your models here.


# class APIRequest(models.Model):
#     content_type = models.CharField(max_length=200)
#     service = models.CharField(max_length=50)
#     location = models.CharField(max_length=50)
#     max_reads = models.IntegerField()
#     image = models.ImageField()
#
#
#
# class Vehicle(models.Model):
#     plate_found = models.BooleanField()
#     plate_country = models.CharField(max_length=3)
#     plate_type_confidence = models.IntegerField()
#     position_confidence = models.IntegerField()
#     plate_chars = models.JSONField()
#     unicode_text = models.CharField(max_length=50)
#     separated_text = models.CharField(max_length=50)
#     engine = models.CharField(max_length=50)
#     proctime = models.IntegerField()
#     confidence = models.IntegerField()
#     plate_roi = models.JSONField()
#     plate_type = models.IntegerField()
#
#     mmr_engine = models.CharField(max_length=50)
#     mmr_found = models.BooleanField()
#     mmr_proctime = models.IntegerField()
#     mmr_category = models.CharField(max_length=50)
#     mmr_category_confidence = models.IntegerField()
#     mmr_color = models.JSONField()
#     mmr_color_confidence = models.IntegerField()
#     mmr_make = models.CharField(max_length=50)
#     mmr_model = models.CharField(max_length=50)
#     mmr_make_confidence = models.IntegerField()
#     mmr_model_confidence = models.IntegerField()
#     mmr_heading = models.CharField(max_length=50)
#     mmr_heading_confidence = models.IntegerField()
#
#     bounds = models.JSONField()

class Vehicle(models.Model):
    data = models.JSONField()

