from django import forms

from tabimport import FileFactory, UnsupportedFileFormat

from .models import Section, Period


class StudentImportForm(forms.Form):
    upload = forms.FileField()

    def __init__(self, file_label='Fichier', mandatory_headers=None, **kwargs):
        super().__init__(**kwargs)
        self.fields['upload'].label = file_label
        self.mandatory_headers = mandatory_headers

    def clean_upload(self):
        f = self.cleaned_data['upload']
        try:
            imp_file = FileFactory(f)
        except UnsupportedFileFormat as e:
            raise forms.ValidationError("Erreur: %s" % e)
        # Check needed headers are present
        headers = imp_file.get_headers()
        missing = set(self.mandatory_headers) - set(headers)
        if missing:
            raise forms.ValidationError("Erreur: il manque les colonnes %s" % (
                ", ".join(missing)))
        return f


class PeriodForm(forms.Form):
    section = forms.ModelChoiceField(queryset=Section.objects.all())
    period = forms.ModelChoiceField(queryset=None)

    def __init__(self, data, *args, **kwargs):
        pass


class UploadHPFileForm(forms.Form):
    upload = forms.FileField(label='Fichier HyperPlanning')


class UploadReportForm(forms.Form):
    semester = forms.ChoiceField(label='Semestre', choices=(('1', '1'), ('2', '2')), required=True)
    upload = forms.FileField(label='Bulletins CLOEE (pdf)')


class EmailBaseForm(forms.Form):
    sender = forms.CharField(widget=forms.HiddenInput())
    to = forms.CharField(widget=forms.TextInput(attrs={'size': '60'}))
    cci = forms.CharField(widget=forms.TextInput(attrs={'size': '60'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'size': '60'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 120}))
