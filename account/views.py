from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from account.forms import UserRegistrationForm, UserProfileForm, PasswordChangeForm


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )

            new_user.save()

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form})


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=True)
            return render(request,
                          'setting/profile.html',
                          {'user_form': form,
                           'alert_message': 'Profile updated successfully — view your profile.'})
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'setting/profile.html', {'user_form': form})


@login_required
def account(request):
    user = request.user

    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)

        if form.is_valid():
            if not form.cleaned_data['old_password']:
                return render(request,
                              'setting/account.html',
                              {'password_from': PasswordChangeForm(),
                               'alert_message': 'Wrong Password'})

            password = form.cleaned_data['new_password2']

            if password:
                user.set_password(password)
                user.save()
                return render(request,
                              'setting/account.html',
                              {'password_form': PasswordChangeForm(),
                               'alert_message': 'Password updated successfully'})


    else:
        form = PasswordChangeForm()

    return render(request, 'setting/account.html', {'password_form': form})