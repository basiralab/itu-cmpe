from django import forms

from .models import Job


class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = '__all__'
        exclude = ('recruiter',)

    def __init__(self, *args, **kwargs):
        super(UpdateJobForm, self).__init__(*args, **kwargs)
        for k, v in self.fields.items():
            # HTML attributes to the form fields can be added here
            v.widget.attrs['class'] = 'form-control'