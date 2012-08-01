from django import forms
from weddings.models import Invitation, WeddingGuest
from django.db.models import Q
from django.utils.crypto import get_random_string
from django.contrib.admin.widgets import FilteredSelectMultiple


class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        exclude = ('invitation_guests', )

    ALLOWED_CHARS = 'ABCDEFGHKMNPQRSTUVWXYZ23456789'

    invite_code = forms.CharField(max_length=10)
    invitation_guests = forms.ModelMultipleChoiceField(widget=FilteredSelectMultiple("Invitation guests", is_stacked=False),
        queryset=WeddingGuest.objects.filter(Q(invitation__isnull=True)), initial=[], required=False)

    def __init__(self, *args, **kwargs):
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields['invite_code'].initial = get_random_string(6, self.ALLOWED_CHARS)
        if self.instance.pk:
            self.fields['invitation_guests'].initial = self.instance.weddingguest_set.all()
            self.fields['invitation_guests'].queryset = WeddingGuest.objects.filter(Q(invitation__isnull=True) | Q(invitation=self.instance.id))

    def save(self, *args, **kwargs):
        instance = super(InvitationForm, self).save(*args, **kwargs)

        instance.save()

        if len(self.fields['invitation_guests'].initial) > 0:
            self.fields['invitation_guests'].initial.update(invitation=None)

        if len(self.cleaned_data['invitation_guests']) > 0:
            self.cleaned_data['invitation_guests'].update(invitation=instance)

        return instance
