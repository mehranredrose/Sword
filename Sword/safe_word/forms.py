from django import forms
from django.forms import TextInput, Select
from .models import CustomUser
from .models import UserSW
non_allowed_usernames = ['abc']
from django.contrib.auth.forms import AuthenticationForm

#The class will store all the required input fields
class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(
            attrs={
                "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        ))
    email = forms.EmailField(widget=forms.EmailInput(
            attrs={
                "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        ))
    password1 = forms.CharField(
        label='Password',
        #The widget handles the rendering of the HTML
        widget=forms.PasswordInput(
            attrs={
                "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        )
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={
                "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            }
        )
    )
    #Check so that passwords match
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("You must confirm your password")
        if password1 != password2:
            raise forms.ValidationError("Your passwords do not match")
        return password2

    def clean_username(self):
        username = self.cleaned_data.get("username")
        #The qs checks if input username matches exactly the User that is already 
        qs = CustomUser.objects.filter(username__iexact=username)
        if username in non_allowed_usernames:
            raise forms.ValidationError("This is an invalid username, please pick another.")
        if qs.exists():
            raise forms.ValidationError("This is an invalid username, please pick another.")
        return username
    
    
    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Email check
        qs = CustomUser.objects.filter(email__iexact=email)
        if qs.exists():
            raise forms.ValidationError("This email is already in use.")
        return email


class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(
        attrs={
            "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
        }
    ))

    def clean_username(self):
        email = self.cleaned_data.get('email')
        qs = CustomUser.objects.filter(email__iexact=email)
        if not qs.exists():
            raise forms.ValidationError("This is an invalid email.")
        return email
    
# class LoginForm(forms.Form):
#     email = forms.EmailField(required=True, widget=forms.EmailInput(
#          attrs={
#          "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
#      }))
#     password = forms.CharField(required=True,
#         widget=forms.PasswordInput(
#             attrs={
#                 "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
#             }
#         )
#     )
    
#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         qs = CustomUser.objects.filter(email__iexact=email) # thisIsMyEmail == thisismyemail
#         if not qs.exists():
#             raise forms.ValidationError("This is an invalid Email.")
#         if qs.count() != 1:
#             raise forms.ValidationError("This is an invalid Email.")
#         return email
    
class UserSWForm(forms.Form):
    PW_TYPES = [('confidential', 'confidential'),('sharable', 'sharable')]
    title = forms.CharField(widget=forms.TextInput(
        attrs={
        "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    }))
    password = forms.CharField(widget=forms.TextInput(
        attrs={
        "class": "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    }))
    type = forms.ChoiceField(choices=PW_TYPES, widget=forms.RadioSelect(
        attrs={
        "class": "grid mt-2 gap-x-[2.75rem] md:grid-cols-2 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500"
    }))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model=UserSW
        fields=['title','password', 'type']
        widgets = {
            'title': TextInput(attrs={
                'class': "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 
                
                #'style': 'max-width: 300px;',
                'placeholder': model.title
                }),
            'password': TextInput(attrs={
                'class': "mb-6 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 
                #'style': 'max-width: 300px;',
                'placeholder': model.password
                }),
            'type': Select(attrs={
                'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500", 
                #'style': 'max-width: 300px;',
                'placeholder': model.type
                })
        }