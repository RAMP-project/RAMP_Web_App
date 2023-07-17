from django import forms


class TimePickerInput(forms.TimeInput):
    input_type = 'time'
