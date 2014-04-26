#!/usr/bin/python2

import calendar
import datetime
import unittest

from course_refs import *
from courses import *

class TestCompatibleCourses(unittest.TestCase):
	def setUp(self):
		c = calendar
		CR = CourseRef
		MT = MeetingTime
		TI = TimeInterval
		T = datetime.time
		C = Course
		CF = CourseFamily
		loc = lecture_only_course

		mwf = (c.MONDAY, c.WEDNESDAY, c.FRIDAY)
		mw = (c.MONDAY, c.WEDNESDAY)

		early_morning = TI(T(8), T(9, 30))
		mid_morning = TI(T(9, 40), T(10, 40))
		late_morning = TI(T(10, 5), T(11, 5))
		morning_to_noon = TI(T(11, 40), T(12, 40))
		noon = TI(T(12), T(13))
		early_afternoon = TI(T(13, 15), T(14, 40))
		late_afternoon = TI(T(14, 20), T(15, 50))
		early_evening = TI(T(16, 40), T(17, 40))
		mid_evening = TI(T(17, 50), T(18, 50))
		late_evening = TI(T(18, 30), T(20, 30))

		meeting_times0 = (MT(c.MONDAY, late_afternoon),)
		meeting_times1 = (MT(c.MONDAY, noon),)
		meeting_times2 = (MT(c.TUESDAY, late_morning),)
		meeting_times3 = (MT(c.TUESDAY, early_morning),)

		self.lecture0 = CR(1, meeting_times0)
		self.lecture1 = CR(2, meeting_times0)
		self.lecture2 = CR(3, meeting_times1)
		self.lecture3a = CR(4, meeting_times0)
		self.lecture3b = CR(5, meeting_times1)
		self.lecture4 = CR(6, meeting_times0)
		self.lecture5a = CR(8, meeting_times0)
		self.lecture5b = CR(10, meeting_times1)

		self.activity4 = CR(7, meeting_times2)
		self.activity5a = CR(9, meeting_times2)
		self.activity5b = CR(11, meeting_times3)

		self.course0 = loc("CS", 101, self.lecture0)
		self.course1 = loc("MUS", 101, self.lecture1)
		self.course2 = loc("MATH", 101, self.lecture2)
		self.course3 = loc("THEA", 101, self.lecture3a, self.lecture3b)
		self.course4 = C("CHEM", 101, (CF((self.lecture4,), (self.activity4,)),))
		self.course5 = C("BIO", 101, (CF((self.lecture5a,), (self.activity5a,)), CF((self.lecture5b,), (self.activity5b,))))

		self.ok_courses = (
			loc("MATH", 314,
				CR(22588, tuple(MT(day, early_morning) for day in mwf)),
				CR(26754, tuple(MT(day, early_morning) for day in mwf))
			),
			loc("AAAS", 282,
				CR(25101, tuple(MT(day, mid_morning) for day in mwf))
			),
			loc("MUS", 217,
				CR(17405, tuple(MT(day, noon) for day in mwf))
			),
			C("CS", 320, (
				CF((CR(24921, tuple(MT(day, noon) for day in mwf)),), (CR(24926, (MT(c.TUESDAY, late_morning),)),)),
				CF((CR(25636, tuple(MT(day, late_afternoon) for day in mw)),), (CR(25653, (MT(c.TUESDAY, early_afternoon),)),))
			)),
			loc("CHIN", 112,
				CR(20289, tuple(MT(day, early_evening) for day in mw))
			),
			C("MUS", 218,(
				CF((CR(17406, (MT(c.TUESDAY, late_morning),)),), (CR(17407, (MT(c.THURSDAY, late_morning),)),)),
				CF((CR(17408, (MT(c.TUESDAY, morning_to_noon),)),), (CR(17409, (MT(c.THURSDAY, morning_to_noon),)),))
			)),
			loc("MUSP", 370,
				CR(14241, (MT(c.TUESDAY, late_evening),))
			),
			loc("MUSP", 371,
				CR(14250, (MT(c.THURSDAY, late_evening),))
			)
		)
		
	def test_trivial_cases(self):
		self.assertFalse(tuple(schedules_from_courses()))
		expected_schedules = (frozenset((self.lecture0,)),)
		self.assertEquals(expected_schedules, tuple(schedules_from_courses(self.course0)))

	def test_small_nontrivial_cases(self):
		# Courses that must meet the same time cannot work
		self.assertFalse(tuple(schedules_from_courses(self.course0, self.course1)))
		# Courses that are compatible
		expected_schedules = (frozenset((self.lecture0, self.lecture2)),)
		self.assertEquals(expected_schedules, tuple(schedules_from_courses(self.course0, self.course2)))
		# Course with different lectures
		expected_schedules = frozenset((frozenset((self.lecture3a,)), frozenset((self.lecture3b,))))
		self.assertEquals(expected_schedules, frozenset(schedules_from_courses(self.course3)))
		# Course with activity
		expected_schedules = (frozenset((self.lecture4, self.activity4)),)
		self.assertEquals(expected_schedules, tuple(schedules_from_courses(self.course4)))
		# Course with two families
		expected_schedules = frozenset((frozenset((self.lecture5a, self.activity5a)), frozenset((self.lecture5b, self.activity5b))))
		self.assertEquals(expected_schedules, frozenset(schedules_from_courses(self.course5)))

	def test_typical_cases(self):
		self.assertEquals(frozenset((
			frozenset((22588, 25101, 17405, 25636, 25653, 20289, 17406, 17407, 14241, 14250)),
			frozenset((22588, 25101, 17405, 25636, 25653, 20289, 17408, 17409, 14241, 14250)),
			frozenset((26754, 25101, 17405, 25636, 25653, 20289, 17406, 17407, 14241, 14250)),
			frozenset((26754, 25101, 17405, 25636, 25653, 20289, 17408, 17409, 14241, 14250))
		)), frozenset(frozenset(cr.number for cr in cr_set) for cr_set in schedules_from_courses(*self.ok_courses)))

if __name__ == "__main__":
	unittest.main()
