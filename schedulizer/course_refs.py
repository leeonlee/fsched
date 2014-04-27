import calendar
import collections
import datetime
import itertools

class TimeInterval(collections.namedtuple("TimeInterval", ("begin", "end"))):
	__slots__ = ()
	def __and__(self, other):
		if self.begin <= other.begin <= self.end <= other.end:
			return TimeInterval(other.begin, self.end)
		elif self.begin <= other.begin <= other.end <= self.end:
			return other
		elif other.begin <= self.begin <= other.end <= self.end:
			return TimeInterval(self.begin, other.end)
		elif other.begin <= self.begin <= self.end <= other.end:
			return self
		else:
			return None

MeetingTime = collections.namedtuple("MeetingTime", ("day", "interval"))
CourseRef = collections.namedtuple("CourseRef", ("number", "times"))

def compatible_time_intervals(*time_intervals):
	l = len(time_intervals)
	return not any(any(time_intervals[i] & time_intervals[j] for j in range(i + 1, l)) for i in range(l))

def compatible_meeting_times(*meeting_times):
	days_of_week_to_intervals = tuple([] for _ in range(7))
	for mt in meeting_times:
		days_of_week_to_intervals[mt.day].append(mt.interval)
	return all(compatible_time_intervals(*interval_list) for interval_list in days_of_week_to_intervals)

def compatible_course_refs(*course_refs):
	return compatible_meeting_times(*itertools.chain.from_iterable(cr.times for cr in course_refs))
