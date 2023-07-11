from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.fields import ArrayField


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_company = models.CharField(max_length=256)


class Usr(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=256, null=True)
    created_date = models.DateField()


class Company(models.Model):
    created_date = models.DateField()
    name = models.CharField(max_length=256)
    url = models.CharField(max_length=256)


class Review(models.Model):
    created_date = models.DateField()
    source_name = models.CharField(max_length=256)
    title = models.CharField(max_length=256)
    description = models.TextField()
    date = models.CharField()
    rate = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)


class Analyze(models.Model):
    created_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name_company = models.CharField(max_length=256, null=True, blank=True)
    avg_rating = models.ImageField(upload_to='analyze', null=True, blank=True)
    rating_distribution = models.ImageField(upload_to='analyze', null=True, blank=True)
    num_reviews_month = models.ImageField(upload_to='analyze', null=True, blank=True)
    num_reviews_country = models.ImageField(upload_to='analyze', null=True, blank=True)
    rating_share_country = models.ImageField(upload_to='analyze', null=True, blank=True)
    bigrams_bad_grades = models.ImageField(upload_to='analyze', null=True, blank=True)
    bigrams_good_grades = models.ImageField(upload_to='analyze', null=True, blank=True)


class DataAnalyze(models.Model):
    name_analyze = models.CharField(max_length=256, null=True, blank=True)
    labels = ArrayField(models.CharField(max_length=256, null=True, blank=True))
    values = ArrayField(models.CharField(max_length=256, null=True, blank=True))
    name_company = models.CharField(max_length=256, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

