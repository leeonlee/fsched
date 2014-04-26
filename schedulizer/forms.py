from django import forms
import autocomplete_light

class CourseForm(forms.Form):
	course = forms.CharField(max_length = 255, widget=autocomplete_light.MultipleChoiceWidget('CourseAutocomplete'))
