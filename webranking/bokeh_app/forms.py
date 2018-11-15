from django import forms
from django.contrib.auth.models import User
from bokeh_app.models import UserInfo, WebInfo
# Create your models here.
# from django.core import validators
# from django.contrib.postgres.fields import IntegerRangeField

# create basic user form
class UserForm(forms.ModelForm):
    # no need for a password at this point
    # password = from.CharField(widget=forms.PasswordInput())

    class Meta():
        model = UserInfo
        fields = ('first_name','last_name','email') #'password', 'username'

class WebForm(forms.ModelForm):
    class Meta():
        model= WebInfo
        fields = ('website',)


# class UserWeb(forms.Form):
#
#     web_name = forms.CharField(max_length=200, required=False)
#     botcatcher = forms.CharField(required=False,
#                                 widget=forms.HiddenInput,
#                                 validators=[validators.MaxLengthValidator(0)])
#     def get_data(self):
#         data = super()
#
#     def clean(self):
#
#         # used to reset and varify data
#         all_clean_data = super().clean()
