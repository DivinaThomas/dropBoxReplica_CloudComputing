from google.appengine.ext import blobstore
from google.appengine.ext import ndb
from google.appengine.ext.webapp import blobstore_handlers
from directory import Directory
import webapp2
import jinja2
import os
from google.appengine.api import users
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class UploadFileHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		error_message = ''
		upload = self.get_uploads()[0]
		blobinfo = blobstore.BlobInfo(upload.key())
		filename = blobinfo.filename
		directory_id = self.request.get('directory_id')
		directory_key = ndb.Key(Directory,directory_id)
		directory = directory_key.get()

		file_exists_counter = 0

		for each in directory.list_of_files :
			if each == filename :
				error_message = 'Sorry a file with this name exists'
				file_exists_counter = file_exists_counter+1
				break

		if file_exists_counter == 0 :
			directory.list_of_files.append(filename)
			directory.blobs.append(upload.key())
			directory.put()
			self.redirect('/')

		else :
			user = users.get_current_user()
			logout = users.create_logout_url('/')
			template_values = {
				'user': user,
				'logout': logout,
				'error_message': error_message,
			}
			template = JINJA_ENVIRONMENT.get_template('error.html')
			self.response.write(template.render(template_values))


