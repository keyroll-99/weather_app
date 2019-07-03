from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserSingInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.check_password(password):
                raise forms.ValidationError('incorrect username or password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserSingInForm, self).clean(*args, **kwargs)

class UserSingUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'password',
        ]
        help_text = {
            'username': None
        }


    def clean(self, *args, **kwargs):

        return super(UserSingUpForm, self).clean(*args, **kwargs)
