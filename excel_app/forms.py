from django import forms
from .models import ExcelFile

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelFile
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': '.xlsx',
                'aria-label': 'Upload Excel file',
            })
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.endswith('.xlsx'):
                raise forms.ValidationError('Only .xlsx files are allowed.')
            return file
