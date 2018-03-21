from django import forms


class SearchForm(forms.Form):
    course_name = forms.CharField(required=False)
    # course_department = forms.ChoiceField(required=False)
    # course_teacher = forms.CharField(required=False)
