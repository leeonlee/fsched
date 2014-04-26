import autocomplete_light

from models import Course, Department

class CourseAutocomplete(autocomplete_light.AutocompleteModelBase):
	autocomplete_js_attributes={'placeholder': 'Enter Course (CS 140)',},
	def choices_for_request(self):
		q = self.request.GET.get('q', '')
	if len(q.split()) == 1:
		choices = Department.objects.filter(name__icontains=q)

autocomplete_light.register(Course, CourseAutocomplete)
