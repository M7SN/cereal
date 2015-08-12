from django import forms
from django.core.validators import RegexValidator
from main.models import Cereal


letter_validator = RegexValidator(r'^[a-zA-Z]*$', 'Please Type Letters')
class CerealSearch(forms.Form):
	name = forms.CharField(required=True, validators=[letter_validator])

class CreateCereal(forms.ModelForm):
	class Meta:
		model = Cereal
		fields = '__all__'


class UserSignUp(forms.Form):
	name = forms.CharField(required = True, validators=[letter_validator])
	email = forms.CharField(required = True)
	password = forms.CharField(widget=forms.PasswordInput(), required = True)

class UserLogin(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)