import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from user import User
from main import Main
from adddirectory import AddDirectory
from deletedirectory import DeleteDirectory
from uploadfilehandler import UploadFileHandler
from addfile import AddFile
from downloadfilehandler import DownloadFileHandler
from deletefile import DeleteFile
from sharefile import ShareFile
from restorefile import RestoreFile
from sharedfiles import SharedFiles

JINJA_ENVIRONMENT = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions = ['jinja2.ext.autoescape'],
	autoescape = True
	)

class Login(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()

		if user :
			self.redirect('/main')

		else :
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication ([
	('/main',Main),
	('/',Login),
	('/adddirectory',AddDirectory),
	('/deletedirectory',DeleteDirectory),
	('/uploadfilehandler',UploadFileHandler),
	('/addfile',AddFile),
	('/downloadfilehandler',DownloadFileHandler),
	('/deletefile',DeleteFile),
	('/sharefile',ShareFile),
	('/restorefile',RestoreFile),
	('/sharedfiles',SharedFiles),
], debug=True)	
