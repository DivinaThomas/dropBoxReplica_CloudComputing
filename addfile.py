import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.api import users
from directory import Directory
from uploadfilehandler import UploadFileHandler
from directory import Directory
import random
from downloadfilehandler import DownloadFileHandler
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class AddFile(webapp2.RequestHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		directory_id = self.request.get('directory_id')
		directory_key = ndb.Key('Directory', directory_id)
		directory = directory_key.get()

		logout = users.create_logout_url('/')
		user = users.get_current_user()
		template_values = {
			'directory_id' : directory_id,
			'user' : user,
			'logout' : logout,
			'upload_url' : blobstore.create_upload_url('/uploadfilehandler'),
		}
		template = JINJA_ENVIRONMENT.get_template('addfile.html')
		self.response.write(template.render(template_values))
