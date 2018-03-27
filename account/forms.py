from django import forms

from account.models import CourseUser


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='密碼',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='重複密碼',
                                widget=forms.PasswordInput)

    email = forms.EmailField()

    class Meta:
        model = CourseUser
        fields = ['username', 'first_name', 'email']
        help_texts = {
            'first_name': '必要的。取個萌萌噠的稱呼也是可以啦。',
            'email': '必要的，請填寫學校的Email，要認證用的喔。',
        }

    def __init__(self, data=None):
        super().__init__(data)
        self.fields['first_name'].required = True
        self.fields['email'].required = True

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data
        if cd['email'].endswith('@alumni.ncyu.edu.tw') or \
           cd['email'].endswith('@mail.ncyu.edu.tw'):
            return cd['email']
        raise forms.ValidationError('Email 必須使用 嘉義大學的Email 註冊')


class UserProfileForm(forms.ModelForm):
    url = forms.URLField(required=False)

    class Meta:
        model = CourseUser
        fields = ['first_name', 'bio', 'url', 'department']

        help_texts = {
            'email': '你可以管理已驗證的email在 email 設定中'
        }


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(label='舊密碼',
                                   widget=forms.PasswordInput)

    new_password = forms.CharField(label='舊密碼',
                                   widget=forms.PasswordInput)

    new_password2 = forms.CharField(label='舊密碼',
                                    widget=forms.PasswordInput)

    def __init__(self, user=None, data=None):
        self.user = user
        super(PasswordChangeForm, self).__init__(data=data)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError('Invalid password')
        return True

    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd['new_password'] != cd['new_password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['new_password2']
