from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
                                label="Логин",
                                widget=forms.TextInput()
    )
    password = forms.CharField(
                               label="Пароль",
                               widget=forms.PasswordInput()
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput()
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput()
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Ник",
        }
        widgets = {
            'email': forms.TextInput(),
            'first_name': forms.TextInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label='Логин',
        widget=forms.TextInput()
    )

    email = forms.CharField(
        disabled=True,
        required=False,
        label='E-mail',
        widget=forms.TextInput()
    )

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name']
        labels = {
            'first_name': 'Ник',
        }
        widgets = {
            'first_name': forms.TextInput(),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput()
    )

    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput()
    )

    new_password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput()
    )
