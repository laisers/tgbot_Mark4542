from django import forms


class BroadcastForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    broadcast_text = forms.CharField(widget=forms.Textarea, label=u'Текст:')


class BulkUploadForm(forms.Form):
    data = forms.CharField(widget=forms.Textarea, label='Данные для загрузки')