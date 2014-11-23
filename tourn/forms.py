from django import forms

from .models import (
    Team,
)


class TeamCreateForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('name', 'admins')
