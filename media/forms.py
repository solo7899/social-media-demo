from django import forms
from .models import Room, Topic
from django.contrib.auth.models import User


class CreateRoomForm(forms.ModelForm):
    # topic = forms.ChoiceField(label="")

    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "required": "true",
            }
        ),
    )

    description = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "required": "false",
                "cols": "30",
                "rows": "3",
            }
        ),
    )

    class Meta:
        model = Room
        fields = [
            "topic",
            "name",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["topic"].widget.attrs[
            "class"
        ] = "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"

        self.fields["topic"].widget.attrs["required"] = "true"


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "required": "true",
            }
        ),
    )
    password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "required": "true",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "required": "true",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already been Used")
        return username


class TopicForm(forms.ModelForm):
    name = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6",
                "required": "true",
            },
        ),
    )

    class Meta:
        model = Topic
        fields = "__all__"

    def clean_name(self):
        name = self.cleaned_data.get("name")
        return name.upper()
