from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import FileExtensionValidator
from .models import PetUser, Post, Comment
from django.contrib.auth.forms import AuthenticationForm


class PetUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    pet_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    pet_type = forms.ChoiceField(
        choices=PetUser.PET_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Тип питомца"
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        label="О вашем питомце"
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])]
    )

    class Meta:
        model = PetUser
        fields = ('username', 'email', 'pet_name', 'pet_type', 'bio', 'avatar', 'password1', 'password2')


class PetUserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']
        widgets = {
            'caption': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Добавьте описание...'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Добавьте комментарий...'
            })
        }
