from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.utils.crypto import get_random_string
from django.conf import settings

def unique_rand():
    while True:
        random_id = get_random_string(length=7)
        # comment for first migration:
        if not RampLoadProfile.objects.filter(random_id=random_id).exists():
            return random_id
        # uncomment for first migration:
        # return random_id


class RampLoadProfile(models.Model):
    name = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    random_id = models.CharField(max_length=7, unique=True, default=unique_rand, null=True)
    load_elec = ArrayField(models.FloatField(null=True), null=True)  # in kWh, one entry per hour
    sum_load_elec = models.FloatField(null=True)  # in kWh
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    ispublic = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class Appliance(models.Model):

    class YesOrNo(models.TextChoices):
        YES = 'yes', _('Ja')
        NO = 'no', _('Nein')

    class WeekendWeekday(models.IntegerChoices):
        WEEKDAY = 0, _('Nur Wochentags')
        WEEKEND = 1, _('Nur am Wochenende')
        ALLWEEK = 2, _('Die ganze Woche lang')


    ramploadprofile = models.ForeignKey(RampLoadProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=1024, null=True)
    number = models.PositiveSmallIntegerField(default=1) #number of appliances of the specified kind
    P = models.FloatField(null=True) # power of one appliance
    num_windows = models.PositiveSmallIntegerField(default=1)
    window_1_start = models.TimeField(null=True)
    window_1_end = models.TimeField(null=True)
    window_2_start = models.TimeField(default='00:00')
    window_2_end = models.TimeField(default='00:00')
    window_3_start = models.TimeField(default='00:00')
    window_3_end = models.TimeField(default='00:00')
    r_w = models.PositiveSmallIntegerField(default=0)  # percentage of variability in the start and ending times of the windows in %
    func_time = models.PositiveSmallIntegerField(null=True)
    r_t = models.PositiveSmallIntegerField(default=0)  # percentage of total time of use that is subject to random variability in %
    func_cycle = models.PositiveSmallIntegerField(default=1) #minimum time the appliance is kept on after switch-on event
    occasional_use = models.PositiveSmallIntegerField(default=100)  # probability that the appliance is always (i.e. everyday) included in the mix of appliances that the user actually switches-on during the day
    wd_we = models.PositiveSmallIntegerField(choices=WeekendWeekday.choices, default=2)



