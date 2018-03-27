from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core import exceptions
from django.conf import settings

# Create your views here.
from account.forms import UserRegistrationForm, UserProfileForm, PasswordChangeForm
from account.models import CourseUser
from account.units.token import Token
from account.tasks import task_send_confirm_email


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)

            new_user.set_password(
                user_form.cleaned_data['password']
            )

            new_user.save()

            token_generate = Token(settings.SECRET_KEY, 'email_confirmation')
            token = token_generate.generate_validate_token(new_user.username)

            subject = "NCYU Course 註冊認証信"
            message = ("Hi, {name}:<br><br>"

                "感謝你的註冊，請點擊下方連結，點擊完後即認證成功。<br>"
                "祝你學業順利:-)<br><br>"

                "帳號:{username} <br><br>"

                "https://{host}/account/email_confirmation?token={token} <br><br>"

                "請勿回覆此信，如有任何疑問請至粉絲頁洽詢（如果有的話），")\
                .format(
                    name= new_user.first_name,
                    username= new_user.username,
                    host= request.get_host(),
                    token= token
                )

            task_send_confirm_email(new_user.email, subject, message)

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

def email_confirmation(request):
    token_confirm = Token(settings.SECRET_KEY, 'email_confirmation')
    token = request.GET['token']

    try:
        username = token_confirm.confirm_validate_token(token)
    except:
        return render(request,
                      'account/email_confirmation.html',
                      {'error_message': 'Token 錯誤或已過期，請再試一次。'})

    try:
        user = CourseUser.objects.get(username=username)
    except exceptions.ObjectDoesNotExist:
        return render(request,
                      'account/email_confirmation.html',
                      {'error_message': '此帳號不存在。'})

    user.is_active = True
    user.save()

    return render(request,
                  'account/email_confirmation.html',
                  {'message': '{} 的 Email 驗證成功'.format(user.first_name)})