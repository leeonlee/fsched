import collections
import itertools

from course_refs import *

CourseFamily = collections.namedtuple("CourseFamily", ("lectures", "activities"))
Course = collections.namedtuple("Course", ("dept", "number", "families",))

def lecture_only_course(dept, number, *lectures):
	return Course(dept, number, (CourseFamily(lectures, ()),))

def schedules_from_course_families(*course_families):
	cr_tuples = tuple( \
		(itertools.product(course_family.lectures, course_family.activities) if course_family.activities \
		else itertools.product(course_family.lectures)) \
		for course_family in course_families \
	)
	cross_family_products = (itertools.product(*cr_tuples)) if cr_tuples else ()
	course_ref_seqs = ((itertools.chain.from_iterable(product)) for product in cross_family_products)
	course_ref_sets = (
		frozenset(course_refs) \
		for course_refs in course_ref_seqs
	)
	return (course_ref_set for course_ref_set in course_ref_sets if compatible_course_refs(*course_ref_set))

def schedules_from_courses(*courses):
	return itertools.chain.from_iterable( \
		schedules_from_course_families(*families)
		for families in itertools.product(*(course.families for course in courses)) \
	)
