from django.shortcuts import render, redirect
from .forms import UserRegisterForm, UserUpdateForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # logs the user in
            username = form.cleaned_data.get('username')
            messages.success(request, _('Account für %(user)s wurde erstellt.') % {'user': username})
            return redirect(request.GET.get('next', 'home')) # either redirects to next page specified in the url or defaults to home
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)

        if uform.is_valid():
            uform.save()
            messages.success(request, _('Das Profil wurde aktualisiert.'))
            return redirect('profile')
    else:
        uform = UserUpdateForm(instance=request.user)

    return render(request, 'users/profile.html', {'uform': uform})

@login_required
def logout_view(request):
    # session data gets deleted after calling the logout function, maybe save and rewrite scenario (to be done)
    logout(request)
    messages.success(request, _('Sie wurden erfolgreich ausgeloggt.'))
    return redirect('home')


class UpdatePassword(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = '/user/edit-profile'
    template_name = 'app/change-password.html'


@login_required
def delete_account(request):
    rem = User.objects.get(username=request.user)
    if rem is not None:
        rem.delete()
        logout(request)
        messages.success(request, _("Ihr Account wurde gelöscht."))
    return redirect('home')
