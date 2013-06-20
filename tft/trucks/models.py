from datetime import datetime, timedelta

from django_extensions.db.models import TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from django.core.urlresolvers import reverse
from django.utils import timezone

from django.contrib.gis.db import models

from django_localflavor_us.models import PhoneNumberField

from accounts.models import User


class CuisineManager(models.Manager):
    def have_companies(self):
        return self.get_query_set().filter(company__gt=1)


class Cuisine(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name', overwrite=True)

    objects = CuisineManager()

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)

    def get_list_url(self):
        return reverse('company_cuisine_list', kwargs={'slug':self.slug})


class CompanyManager(models.Manager):
    def open_trucks(self):
        return self.get_query_set().filter(
            checkins__end_time__gt=timezone.now())
        # return self.get_query_set().filter(checkins__active=timezone.now())


class Company(models.Model):
    name = models.CharField(max_length=250)
    slug = AutoSlugField(populate_from='name')
    description = models.TextField()
    cuisine = models.ManyToManyField(Cuisine)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)

    objects = CompanyManager()

    class Meta:
        verbose_name_plural = 'Companies'

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.slug)

    def get_detail_url(self):
        return reverse('company_detail', kwargs={'slug':self.slug})

    @property
    def open(self):
        """do we have checkins? if so we're open!"""
        return self.checkins.active().exists()


class CompanyLink(models.Model):
    company = models.ForeignKey(Company, related_name='links')
    url = models.URLField()
    TYPE_CHOICES = (('fb', 'facebook'), ('tw', 'twitter'),
                    ('us', 'urban spoon'), ('y', 'yelp'), ('web', 'website'))
    link_type = models.CharField(max_length=5, choices=TYPE_CHOICES)


class Following(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    notify = models.BooleanField(default=True)


class Employee(models.Model):
    company = models.ForeignKey(Company)
    user = models.ForeignKey(User)
    OWNER = 0
    EMPLOYEE = 1
    TITLE_CHOICES = ((OWNER, 'owner'), (EMPLOYEE, 'employee'),)
    title = models.IntegerField(choices=TITLE_CHOICES, default=EMPLOYEE)


class CheckingManager(models.GeoManager):
    def active(self):
        return self.get_query_set().filter(end_time__gt=timezone.now())


class Checkin(TimeStampedModel):
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    company = models.ForeignKey(Company, blank=False, related_name='checkins')
    created_by = models.ForeignKey(User)
    location = models.PointField(srid=4326, blank=True, null=True,
                                 help_text='where your truck is.')

    objects = CheckingManager()

    def __unicode__(self):
        return "%s %s" % (self.company, str(self.location.tuple))
    
    @property
    def time_range(self):
        return self.end_time - self.start_time

    @property
    def time_left(self):
        return timezone.now() - self.end_time

    @property
    def is_active(self):
        return self.time_left().seconds > 0
