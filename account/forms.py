from django import forms
from django.contrib.auth import authenticate, get_user_model

User = get_user_model()

class UserSingInForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get['username']
        password = self.cleaned_data.get['password']

        if username and password:
            user = authenticate(username=username, password=password)
            if not user or not user.check_password(password):
                raise forms.ValidationError('incorrect username or password')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        return super(UserSingInForm, self).clean(*args, **kwargs)

class UserSingUpForm(forms.ModelForm):
    email = forms.EmailField(label='Email Adress')
    email1 = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'email1',
            'password',
        ]

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        email1 = self.cleaned_data.get('email1')

        if email != email1:
            raise forms.ValidationError('email must much')

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError('This email is already being used')

        return super(UserSingUpForm, self).clean(*args, **kwargs)
