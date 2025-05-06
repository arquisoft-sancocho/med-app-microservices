from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class UserCreateForm(UserCreationForm):
    """
    Form for admin users to create new user accounts with role selection
    """
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Group.objects.all(), required=True, label="Rol del Usuario")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "role")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            # Add the user to the selected group/role
            self.cleaned_data["role"].user_set.add(user)

        return user
