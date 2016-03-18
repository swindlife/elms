from django import forms
 
class ImportCSVForm(forms.Form):
    input_file = forms.FileField()
    
    def clean_input_file(self):
        infile = self.cleaned_data.get('input_file', required=True)
        raise ValueError('EEEEE')