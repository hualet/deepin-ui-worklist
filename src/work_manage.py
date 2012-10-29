import json
import os
import fcntl

import gobject

from constant import FILE_WORKLIST, INIT_FILE_WORKLIST
from data_type import Work

class WorkParser:
	total_id = None
	file_dict = None
	work_list = []
	def __init__(self, filename):
		if not os.path.exists(filename):
			print 'file not exsits'
			os.makedirs(os.path.basename(filename))
			f = open(filename, 'w')
			f.write(INIT_FILE_WORKLIST)
			f.close()
		self.filename = filename
	
	def parse(self):
		self.fp = open(self.filename)
		decodedJson = json.load(self.fp)
		self.fp.close()
		WorkParser.file_dict = decodedJson
		WorkParser.total_id = decodedJson["total_id"]
		worklist = decodedJson["work_list"]

		WorkParser.work_list = []
		for work in worklist:
			work_ele = json.loads(json.dumps(work), object_hook=self.json_as_work)
			WorkParser.work_list.append(work_ele)

		return WorkParser.work_list
	
	def _add(self, work):
		workfile_dict = WorkParser.file_dict

		workfile_dict['work_list'].append(self.work_as_json(work))
		workfile_dict['total_id'] = WorkParser.total_id

		workfile = open(self.filename, 'w')
		fcntl.lockf(workfile, fcntl.LOCK_EX)
		json.dump(workfile_dict, workfile)
		fcntl.lockf(workfile, fcntl.LOCK_UN)
		workfile.close()
		self.parse()

		
	def _remove(self, id):
		for work in WorkParser.file_dict['work_list']:
			if work['id'] == id:
				WorkParser.file_dict['work_list'].remove(work)
				workfile = open(self.filename, 'w')
				fcntl.lockf(workfile, fcntl.LOCK_EX)
				json.dump(WorkParser.file_dict, workfile)
				fcntl.lockf(workfile, fcntl.LOCK_UN)
				workfile.close()
				self.parse()

	def _update(self, id, new_work):
		for work in WorkParser.file_dict['work_list']:
			if work['id'] == id:
				WorkParser.file_dict['work_list'].remove(work)
				WorkParser.file_dict['work_list'].append(self.work_as_json(new_work))
				workfile = open(self.filename, 'w')
				fcntl.lockf(workfile, fcntl.LOCK_EX)
				json.dump(WorkParser.file_dict, workfile)
				fcntl.lockf(workfile, fcntl.LOCK_UN)
				workfile.close()

				self.parse()

	def _find(self, title):
		for work in WorkParser.work_list:
			print str(work)
			print work.title == title
			if work.title == title:
				return work


	def json_as_work(self, dct):
		if 'id' not in dct:
			dct['id'] = None
		elif 'start_time' not in dct:
			dct['start_time'] = None
		return Work(dct['title'], dct['time'], 
						dct['content'], dct['id'], dct['start_time'])

	def work_as_json(self, work):
		if not work.id:
			work.id = WorkParser.total_id
			WorkParser.total_id = str(int(WorkParser.total_id) + 1)
		work_dict = {"id":work.id, "title":work.title, 
				"start_time":work.start_time, "time":work.time,
				"content":work.content}
		return work_dict

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
		self.work_parser._add(work)
	def signal_remove(self, manager, id):
		self.work_parser._remove(id)
	def signal_update(self, manager, id, new_work):
		self.work_parser._update(id, new_work)
	def signal_find(self, manager, title):
		self.work_parser._find(title)

	def signal_check_now(self, manager):
		for work in self.worklist:
			work.emit('check-time')

gobject.type_register(WorkManager)

if __name__ == '__main__':
	work_parser = WorkParser(os.path.expanduser(FILE_WORKLIST))
	work_manager = WorkManager(work_parser)

	work_manager.emit('add', Work())
	work_manager.emit('remove', '2')
	work_manager.emit('update', '1', Work(title='work'))
	work_manager.emit('find', 'work')
