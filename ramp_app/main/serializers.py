from rest_framework import serializers
from .models import RampLoadProfile


class RampLoadProfileInputSerializer(serializers.ModelSerializer):

    class Meta:
        model = RampLoadProfile
        exclude = ('date', 'random_id', 'load_elec', 'sum_load_elec', 'user')
