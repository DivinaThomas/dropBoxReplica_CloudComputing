import webapp2
import jinja2
import os
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from directory import Directory
from uploadfilehandler import UploadFileHandler
from directory import Directory
from restore import Restore
from google.appengine.api import users
import random
from downloadfilehandler import DownloadFileHandler
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True
)

class RestoreFile(webapp2.RequestHandler):


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        if self.request.get('button') == 'Bin' :
            email_id = self.request.get('email_id')
            all_files = Restore.query(Restore.user == email_id).fetch()
            user = users.get_current_user()
            logout = users.create_logout_url('/')
            template_values = {
                'all_files': all_files,
                'email_id': email_id,
                'user': user,
                'logout': logout
            }
            template = JINJA_ENVIRONMENT.get_template('restorefile.html')
            self.response.write(template.render(template_values))
        if self.request.get('button') == 'Restore' :
            email_id = self.request.get('email_id')
            file_id = self.request.get('file_id')
            file_key = ndb.Key(Restore,file_id)
            file = file_key.get()

            directory_id = email_id +'/'
            directory_key = ndb.Key(Directory,directory_id)
            directory = directory_key.get()

            directory.list_of_files.append(file.file_name)
            directory.blobs.append(file.blob_key)
            directory.put()

            file_key.delete()
            self.redirect('/main')
