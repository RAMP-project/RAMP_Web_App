from django.forms import ModelForm, NumberInput, FloatField, MultipleChoiceField, IntegerField, CheckboxSelectMultiple, \
ChoiceField, RadioSelect, FloatField, BooleanField, formset_factory, ValidationError, CharField, Select, TimeField, TextInput, BaseFormSet
from .models import RampLoadProfile, Appliance
from django.utils.translation import gettext_lazy as _
from .widgets import TimePickerInput


class RampLoadProfileForm(ModelForm):

    class Meta:
        model = RampLoadProfile
        fields = ('name', )
        labels = {
            'name': _('Name des Haushalts'),
        }
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'})
        }


class ApplianceForm(ModelForm):
    deleted = CharField()

    class Meta:
        model = Appliance
        exclude = ('ramploadprofile',)
        labels = {
            'window_1_start': _('Von'),
            'window_1_end': _('Bis'),
            'window_2_start': _('Von'),
            'window_2_end': _('Bis'),
            'window_3_start': _('Von'),
            'window_3_end': _('Bis'),
            'number': _('Anzahl'),
            'name': _('Name'),
            'P': _('Leistung'),
            'r_t': _('Anteil der Nutzungsdauer mit zufälliger Variablität'),
            'r_w': _('Variabililität in den Zeitfenstern'),
            'func_time': _('Nutzungdauer pro Tag'),
            'func_cycle': _('Mindestnutzungsdauer nach Einschalten'),
            'occasional_use': _('Wahrscheinlichkeit tägliche Nutzung'),
            'wd_we': _('Nutzungszeitraum')
        }
        widgets = {
            'window_1_start': TimePickerInput(attrs={'class': 'form-control'}),
            'window_1_end': TimePickerInput(attrs={'class': 'form-control'}),
            'window_2_start': TimePickerInput(attrs={'class': 'form-control'}),
            'window_2_end': TimePickerInput(attrs={'class': 'form-control'}),
            'window_3_start': TimePickerInput(attrs={'class': 'form-control'}),
            'window_3_end': TimePickerInput(attrs={'class': 'form-control'}),
            'number': NumberInput(attrs={'min': '1', 'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'P': NumberInput(attrs={'class': 'form-control'}),
            'r_w': NumberInput(attrs={'class': 'form-control'}),
            'func_time': NumberInput(attrs={'min': '1', 'class': 'form-control'}),
            'func_cycle': NumberInput(attrs={'class': 'form-control'}),
            'r_t': NumberInput(attrs={'class': 'form-control'}),
            'occasional_use': NumberInput(attrs={'class': 'form-control'}),
            'wd_we': Select(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'number': _('Anzahl der Geräte dieser Art'),
            'name': _('Der Name dient nur zur Unterscheidung für Sie und hat keine Auswirkung auf die Berechnung'),
            'P': _('Elektrische Leistung eines Geräts dieser Art'),
            'r_t': _('Anteil der gesamten Nutzungsdauer, der zufälliger Variabilität unterliegt'),
            'r_w': _('Variabilität in den Start- und Endzeiten der Zeitfenster'),
            'func_time': _('Gesamte Nutzungsdauer pro Tag eines Geräts dieser Art'),
            'func_cycle': _('Mindestdauer, die das Gerät nach Einschalten genutzt wird'),
            'occasional_use': _('Wahrscheinlichkeit, dass das Gerät täglich genutzt wird'),
            'wd_we': _('Um unterschiedliche Nutzungsmuster eines Gerätes am Wochenende und unter Woche zu berücksichtigen, definieren Sie bitte zwei Geräte und wählen Sie einmal "nur wochentags" und einmal "nur am Wochenende".'),
        }

    def clean(self):
        data = self.cleaned_data
        if data['window_1_start'] > data['window_1_end']:
            raise ValidationError(_('Die Startzeit von Zeitfenster 1 muss vor der Endzeit liegen.'))
        if data['window_2_start'] > data['window_2_end']:
            raise ValidationError(_('Die Startzeit von Zeitfenster 2 muss vor der Endzeit liegen.'))
        if data['window_3_start'] > data['window_3_end']:
            raise ValidationError(_('Die Startzeit von Zeitfenster 3 muss vor der Endzeit liegen.'))
        data['window_1_start'] = data['window_1_start'].strftime("%H:%M")
        data['window_1_end'] = data['window_1_end'].strftime("%H:%M")
        data['window_2_start'] = data['window_2_start'].strftime("%H:%M")
        data['window_2_end'] = data['window_2_end'].strftime("%H:%M")
        data['window_3_start'] = data['window_3_start'].strftime("%H:%M")
        data['window_3_end'] = data['window_3_end'].strftime("%H:%M")
        return data

ApplianceFormSet = formset_factory(form=ApplianceForm, min_num=0, extra=0, max_num=30)
