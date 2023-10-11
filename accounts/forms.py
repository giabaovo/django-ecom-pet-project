from typing import Any
from django import forms

from accounts.models import Account, UserProfile

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Enter Confirm Password"}))
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "email", "phone_number", "password"]

    def clean(self):
        cleand_data = super(RegisterForm, self).clean()
        password = cleand_data.get("password")
        confirm_password = cleand_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("The password is not matching")
        return cleand_data
    
    # def clean_email(self):
    #     email = self.cleaned_data.get("email")
    #     is_exist = Account.objects.filter(email=email).exists()




    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["placeholder"] = "Enter First Name"
        self.fields["last_name"].widget.attrs["placeholder"] = "Enter Last Name"
        self.fields["email"].widget.attrs["placeholder"] = "Enter Email Address"
        self.fields["phone_number"].widget.attrs["placeholder"] = "Enter Phone Number"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "phone_number"]

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class UserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False, error_messages={"invalid": ("Image file only")}, widget=forms.FileInput)
    class Meta:
        model = UserProfile
        fields = ["address_line_1", "address_line_2", "profile_picture", "country", "state", "city"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"