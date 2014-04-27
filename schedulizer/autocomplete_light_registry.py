import autocomplete_light

from models import Course, Department

class CourseAutocomplete(autocomplete_light.AutocompleteModelBase):
	autocomplete_js_attributes={'placeholder': 'Enter Course (CS 140)', 'max_values': 2,}
	def choices_for_request(self):
		q = self.request.GET.get('q', '')
		choices = Department.objects.all()
		if len(q.split()) == 1:
			choices = Department.objects.filter(name__icontains=q.upper())
		if len(q.split()) == 2:
			dept, num = q.split()
			choices = Course.objects.filter(department = Department.objects.get(name=dept.upper()), name__startswith=num)
			courses = [choice.name for choice in choices]
			courses = list(set(courses))
			choices = [Course.objects.filter(department=Department.objects.get(name=dept.upper()), name=name)[0] for name in courses]

		return choices

autocomplete_light.register(Course, CourseAutocomplete)
