#!/usr/bin/env python

import gtk
import gobject
from theme_init import app_theme
from dtk.ui.application import Application


class WorkListApp(gobject.GObject):
	def __init__(self):
		gobject.GObject.__init__(self)
		
		self.app = Application(False)
		self.app.window.set_size_request(500, 300)
		# Add app titlebar.
		self.app.add_titlebar(["theme", "menu", "max", "min", "close"],
								None, "WorkList for Deepin", " ", 
								add_separator = True)        
		self.app.set_icon(app_theme.get_pixbuf('icon/worklist.png'))
		self.app.set_skin_preview(app_theme.get_pixbuf('frame.png'))

		self.win = self.app.window
		self.win.set_resizable(False)
		self.app.run()
 
if __name__ == '__main__':
	WorkListApp()
