#!/usr/bin/python2

import calendar
import datetime
import unittest

from course_refs import *

class TestCompatibleCourseRefs(unittest.TestCase):
	def setUp(self):
		c = calendar
		CR = CourseRef
		MT = MeetingTime
		TI = TimeInterval
		T = datetime.time

		mwf = (c.MONDAY, c.WEDNESDAY, c.FRIDAY)
		mw = (c.MONDAY, c.WEDNESDAY)

		early_morning = TI(T(8), T(9, 30))
		mid_morning = TI(T(9, 40), T(10, 40))
		late_morning = TI(T(10, 5), T(11, 5))
		morning_to_noon = TI(T(11), T(12))
		noon = TI(T(12), T(13))
		early_afternoon = TI(T(13, 15), T(14, 40))
		late_afternoon = TI(T(14, 20), T(15, 50))
		early_evening = TI(T(16, 40), T(17, 40))
		mid_evening = TI(T(17, 50), T(18, 50))
		late_evening = TI(T(18, 30), T(20, 30))
		
		self.good_course_refs = (
			CR(22588, (MT(day, early_morning) for day in mwf)),
			CR(25101, (MT(day, mid_morning) for day in mwf)),
			CR(17405, (MT(day, noon) for day in mwf)),
			CR(25636, (MT(day, late_afternoon) for day in mw)),
			CR(20289, (MT(day, early_evening) for day in mw)),
			CR(17406, (MT(c.TUESDAY, late_morning),)),
			CR(17407, (MT(c.THURSDAY, late_morning),)),
			CR(25653, (MT(c.TUESDAY, early_afternoon),)),
			CR(14241, (MT(c.TUESDAY, late_evening),)),
			CR(14250, (MT(c.THURSDAY, late_evening),)),
		)

		self.bad_course_refs0 = (
			CR(22588, (MT(day, early_morning) for day in mwf)),
			CR(25101, (MT(day, mid_morning) for day in mwf)),
			CR(17405, (MT(day, noon) for day in mwf)),
			CR(25636, (MT(day, late_afternoon) for day in mw)),
			CR(20289, (MT(day, early_evening) for day in mw)),
			CR(17406, (MT(c.TUESDAY, late_morning),)),
			CR(17407, (MT(c.THURSDAY, late_morning),)),
			CR(25653, (MT(c.TUESDAY, mid_evening),)), # only difference with good_course_refs
			CR(14241, (MT(c.TUESDAY, late_evening),)),
			CR(14250, (MT(c.THURSDAY, late_evening),)),
		)

		self.bad_course_refs1 = (
			CR(22588, (MT(day, early_morning) for day in mwf)),
			CR(25101, (MT(day, mid_morning) for day in mwf)),
			CR(17405, (MT(day, noon) for day in mwf)),
			CR(24921, (MT(day, late_afternoon) for day in mw)),
			CR(20289, (MT(day, early_evening) for day in mw)),
			CR(17406, (MT(c.TUESDAY, late_morning),)),
			CR(17407, (MT(c.THURSDAY, late_morning),)),
			CR(25653, (MT(c.TUESDAY, morning_to_noon),)), # diff
			CR(14241, (MT(c.TUESDAY, late_evening),)),
			CR(14250, (MT(c.THURSDAY, late_evening),)),
		)

		self.bad_course_refs2 = (
			CR(22588, (MT(day, early_morning) for day in mwf)),
			CR(25101, (MT(day, mid_morning) for day in mwf)),
			CR(17405, (MT(day, noon) for day in mwf)),
			CR(24921, (MT(day, noon) for day in mwf)), # diff
			CR(20289, (MT(day, early_evening) for day in mw)),
			CR(17406, (MT(c.TUESDAY, late_morning),)),
			CR(17407, (MT(c.THURSDAY, late_morning),)),
			CR(24926, (MT(c.TUESDAY, late_morning),)), # diff
			CR(14241, (MT(c.TUESDAY, late_evening),)),
			CR(14250, (MT(c.THURSDAY, late_evening),)),
		)

	def test_trivial_cases(self):
		self.assertTrue(compatible_course_refs())
		mt = MeetingTime(calendar.MONDAY, TimeInterval(datetime.time(), datetime.time(1)))
		cr = CourseRef(0, (mt,))
		self.assertTrue(compatible_course_refs(cr))
		self.assertFalse(compatible_course_refs(cr, CourseRef(1, (mt,))))
		self.assertFalse(compatible_course_refs(CourseRef(1, (mt,)), cr))

	def test_typical_cases(self):
		self.assertTrue(compatible_course_refs(*self.good_course_refs))
		self.assertFalse(compatible_course_refs(*self.bad_course_refs0))
		self.assertFalse(compatible_course_refs(*self.bad_course_refs1))
		self.assertFalse(compatible_course_refs(*self.bad_course_refs2))

if __name__ == "__main__":
	unittest.main()
