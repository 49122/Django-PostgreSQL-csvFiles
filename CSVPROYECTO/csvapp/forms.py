from django import forms

class Rowform(forms.Form):
    csv_name = forms.CharField(label='csv name', max_length=75)
    dataset_id = forms.IntegerField()
    #point