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

class ShareFile(webapp2.RequestHandler):
	def post(self):
            self.response.headers['Content-Type'] = 'text/html'
            if self.request.get('button') == 'Share':
                directory_id = self.request.get('directory_id')
                share_file_name = self.request.get('share_file_name')
                index = self.request.get('index')
                owner_email_id = self.request.get('owner_email_id')
                user = users.get_current_user()
                logout = users.create_logout_url('/')
                template_values = {
                    'share_file_name' : share_file_name,
                    'directory_id': directory_id,
                    'index' : index,
                    'owner_email_id' : owner_email_id,
                    'user': user,
                    'logout': logout
                    # 'upload_url': blobstore.create_upload_url('/uploadfilehandler'),
                }
                template = JINJA_ENVIRONMENT.get_template('sharefile.html')
                self.response.write(template.render(template_values))

            if self.request.get('button') == 'Check email_id' :
                directory_id = self.request.get('directory_id')
                share_file_name = self.request.get('share_file_name')
                index = int(self.request.get('index'))
                email_id = self.request.get('email_id')
                directory_key = ndb.Key(Directory,directory_id)
                directory = directory_key.get()
                blob_key = directory.blobs[index]
                owner_email_id = self.request.get('owner_email_id')
                user_counter = 0
                id = email_id + '/'
                shared_user_key = ndb.Key(Directory,id)
                shared_user = shared_user_key.get()
                user = users.get_current_user()
                logout = users.create_logout_url('/')
                if shared_user == None :
                     error_message = 'Sorry a user with this email id does not exists. Please check the email id'

                     template_values = {
                         'error_message' : error_message,
                         'user' : user,
                         'logout' : logout
                     }
                     template = JINJA_ENVIRONMENT.get_template('error.html')
                     self.response.write(template.render(template_values))
                #all_directories = Directory.query.fetch()
                #for each_directory in all_directories :
                 #   if each_directory.id == key :
                  #      user_counter = user_counter + 1
                   #     break
                else :
                    shared_user.shared_files.append(share_file_name)
                    shared_user.shared_files_blobs.append(blob_key)
                    shared_user.shared_file_owner.append(owner_email_id)
                    shared_user.put()
                    self.redirect('/main')
                #if user_counter > 0 :
