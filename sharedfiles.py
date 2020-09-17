import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb

import os
from user import User
from directory import Directory

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class SharedFiles(webapp2.RequestHandler):
    def post(self):
        email_id =self.request.get('email_id')
        SharedFiles = []
        SharedFileOwner = []
        id = email_id + '/'
        key = ndb.Key(Directory, id)
        dir = key.get()
        for index, each in enumerate(dir.shared_files):
            SharedFiles.append(each)
            owner = dir.shared_file_owner[index]
            SharedFileOwner.append(owner)
        user = users.get_current_user()
        logout = users.create_logout_url('/')
        template_values = {
            'id_of_root_directory': id,
            'logout': logout,
            'user' : user,
            'shared_files' : SharedFiles,
            'shared_file_owner' : SharedFileOwner
        }

        template = JINJA_ENVIRONMENT.get_template('sharedfiles.html')
        self.response.write(template.render(template_values))
