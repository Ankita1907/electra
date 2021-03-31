from django import forms
from.models import Response

class ResponseForm(forms.Form):
    Ans = forms.CharField()

class CommentForm(forms.Form):
    comment = forms.CharField()
    point = forms.IntegerField()