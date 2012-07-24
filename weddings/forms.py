from django import forms
from weddings.models import Invitation, WeddingGuest
from django.utils.crypto import get_random_string


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation

    ALLOWED_CHARS = 'ABCDEFGHKMNPQRSTUVWXYZ23456789'

    invite_code = forms.CharField(max_length=10, initial=get_random_string(6, ALLOWED_CHARS))
    invitation_guests = forms.ModelMultipleChoiceField(queryset=WeddingGuest.objects.all())

    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['invitation_guests'].initial = self.instance.weddingguest_set.all()

    def save(self, *args, **kwargs):
        instance = super(InvitationForm, self).save(commit=False)
        self.fields['invitation_guests'].initial.update(invitation=None)
        self.cleaned_data['invitation_guests'].update(invitation=instance)
        return instance
