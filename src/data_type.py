import gobject
import datetime

class Work(gobject.GObject):
	__gsignals__ = {
		"check-time" : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
	}

	def __init__(self, title=None, time=None, 
							content=None, id=None, start_time=None):
		gobject.GObject.__init__(self)
		self.title = title
		if start_time == None:
			self.start_time = TimeFormatter.get_now_time()
		else:
			self.start_time = start_time
		self.time = time
		self.content = content
		self.id = id

		self.connect('check-time', self.check_time)

	def get_formatted_start_time(self):
		return TimeFormatter(self.start_time).format_time()
	def get_formatted_alarm_time(self):
		return TimeFormatter(self.time).format_time()

	def check_time(self, work):
		print 'check_time'

	def __str__(self):
		return 'id : %s, title : %s, start_time : %s, time : %s, content : %s'\
			% (str(self.id), self.title, self.start_time, 
				self.time, self.content)


class TimeFormatter():
	def __init__(self, time_str):
		self._time_str = time_str
	
	def format_time(self):
		if self._time_str != None and self._time_str != '':
			timetuple = self._time_str.split('-')
			timetuple = [int(x) for x in timetuple]
			date = datetime.datetime(*timetuple)

			if len(timetuple) == 3:
				return date.strftime('%x')

			return date.strftime('%x, %H:%M')
		else:
			return ''

	@classmethod
	def get_now_time(cls):
		"""
		get the time now and format it in 'year-month-day-hour-minute'
		"""

		now_time = datetime.datetime.now()
		timetuple = [now_time.year, now_time.month, now_time.day, 
							now_time.hour, now_time.minute]
		return '-'.join([str(x) for x in timetuple])

gobject.type_register(Work)
