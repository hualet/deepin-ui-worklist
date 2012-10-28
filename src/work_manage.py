import json
import os
import fcntl

import gobject

from data_type import Work

class WorkParser:
	total_id = None
	work_list = []
	def __init__(self, filename):
		if not os.path.exists(filename):
			print 'file not exsits'
			os.makedirs(os.path.basename(filename))
			open(filename, 'w').close()
		self.filename = filename
	
	def parse(self):
		self.fp = open(self.filename)
		decodedJson = json.load(self.fp)
		global total_id
		total_id = decodedJson["total_id"]
		worklist = decodedJson["work_list"]

		for work in worklist:
			work_ele = json.loads(json.dumps(work), object_hook=self.json_as_work)
			WorkParser.work_list.append(work_ele)

		return WorkParser.work_list
	
	def add(self, work):

		workfile = open(self.filename, 'r')
		workfile_dict = json.load(workfile)

		workfile_dict['total_id'] = self.total_id
		workfile_dict['work_list'].append(self.work_as_json(work))
		workfile.close()
		workfile = open(self.filename, 'w')
		fcntl.lockf(workfile, fcntl.LOCK_EX)
		json.dump(workfile_dict, workfile)
		fcntl.lockf(workfile, fcntl.LOCK_UN)
		workfile.close()

		
	def remove(self, id):
		print 'remove'  + str(id)
	def update(self, id, new_work):
		print 'update' + str(new_work)
	def find(self, title):
		print 'find' + title


	def json_as_work(self, dct):
		if 'id' not in dct:
			dct['id'] = None
		elif 'start_time' not in dct:
			dct['start_time'] = None
		return Work(dct['title'], dct['time'], 
						dct['content'], dct['id'], dct['start_time'])

	def work_as_json(self, work):
		if not work.id:
			work.id = self.total_id
			self.total_id = str(int(self.total_id) + 1)
		work_dict = {"id":work.id, "title":work.title, 
				"start_time":work.start_time, "time":work.time,
				"content":work.content}
		return json.dump(work_dict)

class WorkManager(gobject.GObject):
	__gsignals__ = {
		'add' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (Work,)),
		'remove' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str,)),
		'update' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str, Work)),
		'find' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (str,)),
		'check-now' : (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE,()),
	}

	def __init__(self, work_parser):
		gobject.GObject.__init__(self)
		self.work_parser = work_parser

		self.worklist = self.work_parser.parse()

		self.connect('add', self.signal_add)
		self.connect('remove', self.signal_remove)
		self.connect('update', self.signal_update)
		self.connect('find', self.signal_find)
		self.connect('check-now', self.signal_check_now)

	def signal_add(self, manager, work):
		self.work_parser.add(work)
	def signal_remove(self, manager, id):
		self.work_parser.remove(id)
	def signal_update(self, manager, id, new_work):
		self.work_parser.update(id, new_work)
	def signal_find(self, manager, title):
		self.work_parser.find(title)

	def signal_check_now(self, manager):
		for work in self.worklist:
			work.emit('check-time')

gobject.type_register(WorkManager)

if __name__ == '__main__':
	work_parser = WorkParser(os.path.expanduser('~/Desktop/test.txt'))
	work_manager = WorkManager(work_parser)

	work_manager.emit('add', Work())
	work_manager.emit('remove', 2)
	work_manager.emit('update', 2, Work())
	work_manager.emit('find', 'title')
