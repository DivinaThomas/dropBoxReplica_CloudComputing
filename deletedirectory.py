import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

import os
from user import User
from directory import Directory
import random

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class DeleteDirectory(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Delete' :
			directory_id = self.request.get('directory_id')
			directory_key = ndb.Key('Directory',directory_id)
			directory = directory_key.get()
		#	template_values = {
		#	'directory_id' : directory,
		#	}
#
#			template = JINJA_ENVIRONMENT.get_template('adddirectory.html')
#			self.response.write(template.render(template_values))

			delete_directory_name = self.request.get('delete_directory_name')
			delete_counter = 0
			for index,each in enumerate(directory.list_of_directories) :
				preprocessed_id = each.replace('u','').replace(' ','').replace('\'','')
				sub_directory_key = ndb.Key(Directory,preprocessed_id)
				sub_directory = sub_directory_key.get()
				if sub_directory.directory_name == delete_directory_name:
					if sub_directory.list_of_files == [] :
						if sub_directory.list_of_directories == [] :
							sub_directory_key.delete()
							del directory.list_of_directories[index]
							directory.put()
							delete_counter = delete_counter + 1
							break

			if delete_counter > 0:
				self.redirect('/main')

			else :
				user = users.get_current_user()
				logout = users.create_logout_url('/')
				error_message = 'This directory has files or directories in it so it cant be deleted'
				template_values = {
					# 'collection' : new_file,
					'error_message': error_message,
					'user' : user,
					'logout' : logout
					# 'directory_id' : directory_id,
					# 'upload_url': blobstore.create_upload_url('/uploadfilehandler'),
				}
				template = JINJA_ENVIRONMENT.get_template('error.html')
				self.response.write(template.render(template_values))
