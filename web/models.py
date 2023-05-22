from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()


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
    date = models.DateField()
    rate = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    usr = models.ForeignKey(Usr, on_delete=models.CASCADE)


class Analyze(models.Model):
    created_date = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    avg_rating = models.ImageField(upload_to='analyze', null=True, blank=True)
    rating_distribution = models.ImageField(upload_to='analyze', null=True, blank=True)
    num_reviews_month = models.ImageField(upload_to='analyze', null=True, blank=True)
    num_reviews_country = models.ImageField(upload_to='analyze', null=True, blank=True)
    rating_share_country = models.ImageField(upload_to='analyze', null=True, blank=True)
    bigrams_bad_grades = models.ImageField(upload_to='analyze', null=True, blank=True)
    bigrams_good_grades = models.ImageField(upload_to='analyze', null=True, blank=True)
