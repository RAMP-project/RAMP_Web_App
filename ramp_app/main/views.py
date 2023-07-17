from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RampLoadProfileForm, ApplianceForm, ApplianceFormSet
from .models import RampLoadProfile, Appliance
import numpy as np
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ugettext
from django.contrib import messages
import io
import re
import xlsxwriter
from django.utils import timezone, dateformat
from django.conf import settings
from .serializers import RampLoadProfileInputSerializer
from .run_ramp import run_ramp


def string_is_safe(string):
    return bool(re.compile(r'^[A-za-z0-9]+\Z').match(string))

def start(response):
    if response.method == 'POST':
        # retrieve user preference regarding the use of a template
        if 'load_profile' in response.POST:
            lp_id = response.POST['load_profile']
        else:
            lp_id = '0'
        # 0=start without template, otherwise id corresponds to model ids in DB
        if lp_id != '0':
            if len(lp_id) == 7 and string_is_safe(lp_id):
                # check if random_id is in database
                if not RampLoadProfile.objects.filter(random_id=lp_id).exists():
                    messages.add_message(response, messages.ERROR,
                                         _('Das Lastprofil mit der Kennung %(id)s wurde nicht gefunden.') % {
                                             'id': lp_id})
                    return HttpResponseRedirect(reverse('ramp_start'))
                # retrieve data from database
                r = RampLoadProfile.objects.get(random_id=lp_id)
                # check if scenario belongs to logged in user or the owner shared it
                if not response.user == r.user and not r.ispublic:
                    messages.add_message(response, messages.ERROR,
                                         _('Das Szenario mit der Kennung %(id)s kann nicht verwendet werden.') % {
                                             'id': lp_id})
                    return HttpResponseRedirect(reverse('ramp_start'))
            else:
                messages.add_message(response, messages.ERROR,
                                     _('Die Kennung hat nicht das richtige Format.'))
                return HttpResponseRedirect(reverse('ramp_start'))
            # save to session
            response.session['ramp_scenario'] = {}
            response.session['ramp_scenario']['RampLoadProfile'] = RampLoadProfileInputSerializer(instance=r).data
            all_apps = list(r.appliance_set.all().values())
            for data in all_apps:
                data['window_1_start'] = data['window_1_start'].strftime("%H:%M")
                data['window_1_end'] = data['window_1_end'].strftime("%H:%M")
                data['window_2_start'] = data['window_2_start'].strftime("%H:%M")
                data['window_2_end'] = data['window_2_end'].strftime("%H:%M")
                data['window_3_start'] = data['window_3_start'].strftime("%H:%M")
                data['window_3_end'] = data['window_3_end'].strftime("%H:%M")
            response.session['ramp_scenario']['Appliances'] = all_apps
        else:  # lp_id = 0
            # delete previous scenario in session
            response.session['ramp_scenario'] = {}
        # get Django to recognize the changes made
        response.session.modified = True
        # redirect to input page
        return HttpResponseRedirect(reverse('ramp_input'))
    # show start page with templates
    # get public templates from database
    public_temps = RampLoadProfile.objects.all().filter(ispublic=True)
    # if user is logged in, additionally get their templates
    if response.user.is_authenticated:
        user_temps = RampLoadProfile.objects.all().filter(user=response.user)
    else:
        user_temps = {}
    # database retrieval
    return render(response, "main/start.html", {'public_temps': public_temps, 'user_temps': user_temps})


def input(response):
    if response.method == 'POST':
        lp_form = RampLoadProfileForm(response.POST)
        appliance_formset = ApplianceFormSet(response.POST)
        if lp_form.is_valid():
            response.session['ramp_scenario'] = {}
            response.session['ramp_scenario']['RampLoadProfile'] = lp_form.cleaned_data
            if appliance_formset.is_valid():
                # do a bit of hacking here to delete forms that were deleted in the front end..
                data_new = []
                for form in appliance_formset.cleaned_data:
                    if form['deleted'] == 'false':
                        form_copy = form.copy()
                        form_copy.pop('deleted')
                        data_new.append(form_copy)
                response.session['ramp_scenario']['Appliances'] = data_new
                response.session.modified = True
                # use ramp here
                load_elec = run_ramp(data_new)
                # for testing generate empty lp
                sum_load_elec = round(sum(load_elec), 2)
                # save to session
                response.session['ramp_scenario']['RampLoadProfile']['load_elec'] = load_elec
                response.session['ramp_scenario']['RampLoadProfile']['sum_load_elec'] = sum_load_elec

                response.session.modified = True
                # redirect to the next page, reverse() is needed to preserve language prefix in url
                return HttpResponseRedirect(reverse('ramp_result'))
            else:
                messages.add_message(response, messages.INFO,
                                     _('Beim Prüfen der Eingaben sind Fehler aufgetreten. Bitte beheben Sie diese.'))
    else:
        lp_form = RampLoadProfileForm(initial=response.session.get('ramp_scenario', {}).get('RampLoadProfile'))
        appliance_formset = ApplianceFormSet(initial=response.session.get('ramp_scenario', {}).get('Appliances'))
    return render(response, "main/input.html", {'lp_form': lp_form, 'appliance_formset': appliance_formset})


def result(response):
    if response.method == 'POST':
        # saving was requested
        if response.user.is_authenticated:
            # redirect to save scenario
            return redirect(reverse('ramp_save'))
        else:  # user is not logged in
            # redirect to login page and 'save' after that
            # add message that is displayed in the login view
            messages.add_message(response, messages.INFO,
                                 _('Bitte loggen Sie sich zunächst ein.'))
            # redirect to login page
            return redirect('%s?next=%s' % (reverse(settings.LOGIN_URL), reverse('ramp_save')))
        pass
    # get results from session
    load_elec = response.session.get('ramp_scenario', {}).get('RampLoadProfile', {}).get('load_elec', None)
    sum_load_elec = response.session.get('ramp_scenario', {}).get('RampLoadProfile', {}).get('sum_load_elec', None)
    return render(response, "main/result.html", {'load_elec': load_elec,
                                                 'sum_load_elec': sum_load_elec})


def save(response):
    # only gets called if the user is logged in
    # check if user is really authenticated
    if response.user.is_authenticated:
        # check if results in session
        if 'load_elec' in response.session.get('ramp_scenario', {}).get('RampLoadProfile', {}):
            ramp_lp_data = response.session['ramp_scenario']['RampLoadProfile']
            r = RampLoadProfile.objects.create(user=response.user, **ramp_lp_data)
            appliances_data = response.session['ramp_scenario']['Appliances']
            for app_data in appliances_data:
                a = Appliance.objects.create(ramploadprofile=r, **app_data)
            # add message, that saving was successful
            messages.add_message(response, messages.SUCCESS,
                                 _('Speichern war erfolgreich. Rufen Sie das Dashboard (oben rechts im Nutzermenü) auf, um gespeicherte '
                                   'Lastprofile jederzeit downzuloaden oder zu löschen.'))
            return HttpResponseRedirect(reverse('ramp_result'))
    # saving was not successful: add error message and redirect to result
    messages.add_message(response, messages.ERROR,
                         _('Beim Speichern ist ein Fehler aufgetreten. Bitte versuchen Sie es erneut.'))
    return HttpResponseRedirect(reverse('ramp_result'))


def download(response):
    # check if results in session
    if 'load_elec' in response.session.get('ramp_scenario', {}).get('RampLoadProfile', {}):
        # retrieve data from session
        name = response.session['ramp_scenario']['RampLoadProfile']['name']
        load_elec = response.session['ramp_scenario']['RampLoadProfile']['load_elec']
        response = write_excel(response, name, load_elec)

        return response
    # add message that something went wrong i the future
    return HttpResponse(status=204)  # empty response for now


def write_excel(response, name, load_elec):
    # create output file in memory
    # create workbook variable to write Session data into Excel sheets
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    worksheet.write_column(0, 0, load_elec)
    load_hot_water_helper = np.zeros(8760)
    load_hot_water_helper2 = load_hot_water_helper.tolist()
    worksheet.write_column(0,1, load_hot_water_helper2)
    workbook.close()

    output.seek(0)
    response = HttpResponse(output.read(),
                            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    name_cleaned = name.replace(" ,", "_")
    name_cleaned2 = name_cleaned.replace(" ","_")
    name_cleaned3 = name_cleaned2.replace("/", "")
    name_cleaned4 = name_cleaned3.replace(".","")
    filename = "RAMP_" + ugettext("Lastprofil_") + f"{name_cleaned4}_" + dateformat.format(timezone.now(), 'Y-m-d_H-i-s')
    response['Content-Disposition'] = f"attachment; filename={filename}.xlsx"

    output.close()
    return response

@login_required(redirect_field_name='login')
def saved_profiles(response):
    if response.method == 'POST':
        if 'delete' in response.POST:
            # retrieve id of result that should be deleted
            id = response.POST['delete']
            # get result object
            r = RampLoadProfile.objects.get(id=id)
            name = r.name
            # check again, if user is owner of the result
            if response.user == r.user:
                # delete object
                r.delete()
                # add message to display
                messages.add_message(response, messages.SUCCESS,
                                     ugettext('Das Lastprofil %(name)s wurde erfolgreich gelöscht.') % {'name': name})
            return HttpResponseRedirect(reverse('saved_profiles'))
        elif 'download' in response.POST:
            id = response.POST['download']
            r = RampLoadProfile.objects.get(id=id)
            response = write_excel(response, r.name, r.load_elec)
            return response
    # database retrieval
    load_profiles = RampLoadProfile.objects.all().filter(user=response.user)
    return render(response, "main/saved_profiles.html", {'load_profiles': load_profiles})
